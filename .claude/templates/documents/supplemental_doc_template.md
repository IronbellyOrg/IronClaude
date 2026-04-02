---
id: "GFXAI-[TOPIC-NAME]"
title: "[Human Readable Title]"
description: "[One-sentence summary - must match FILE_INVENTORY_STATUS entry]"
version: "1.0"
status: "📝 Template"
type: "📑 Reference"
priority: "▶️ Medium"
created_date: "YYYY-MM-DD"
updated_date: "YYYY-MM-DD"
assigned_to: "[team-name]"
autogen: false
autogen_method: ""
coordinator: ""
parent_task: ""
depends_on: []
related_docs:
- [path/to/parent-doc.md]
- [path/to/related-doc-1.md]
- [path/to/related-doc-2.md]
tags:
- tag1
- tag2
- tag3
template_schema_doc: ""
estimation: ""
sprint: ""
due_date: ""
start_date: ""
completion_date: ""
blocker_reason: ""
ai_model: ""
model_settings: ""
review_info:
  last_reviewed_by: ""
  last_review_date: ""
  next_review_date: ""
task_type: "static"
---

# [Document Title]

← Back to [parent_doc_title](../path/to/parent.md)

> **WHAT:** [One sentence describing what this document contains]
> **WHY:** [One sentence explaining why this document exists and its value]
> **HOW TO USE:** [One sentence on who should use it and when]

### Document Lifecycle Position

**Standalone document** — not part of the PRD → TDD → Tech Ref lifecycle.

### Tiered Usage

| Tier | When to Use | Sections Required |
|------|-------------|-------------------|
| **Lightweight** | Quick reference with <5 sections | Core sections only; omit Appendices, abbreviate Completeness Status to 1-line note, omit Document History for first version |
| **Standard** | Typical reference with 5-10 sections | All universal sections; full Completeness Status and Contract Table |
| **Heavyweight** | Comprehensive reference with 10+ sections | All sections; full Appendices; detailed Document History |

---

## Document Information

| Field | Value |
|-------|-------|
| **Document Name** | [Name] |
| **Document Type** | General Reference |
| **Maintained By** | [Team or person] |
| **Last Verified** | [Date and context — e.g., "2026-03-08 against commit b00251b7"] |

---

## Completeness Status

**Completeness Checklist:**
- [ ] Section 1 documented - **To Do**
- [ ] Section 2 documented - **To Do**
- [ ] Section 3 documented - **To Do**
- [ ] Section 4 documented - **To Do**
- [ ] Section 5 documented - **To Do**
- [ ] All links verified - **To Do**
- [ ] Reviewed by [team-name] - **Pending team review**

**Contract Table:**

| Element | Details |
|---------|---------|
| **Dependencies** | [Parent/anchor docs this depends on] |
| **Upstream** | Feeds from: [docs that provide input] |
| **Downstream** | Feeds to: [systems/teams/docs that consume this] |
| **Change Impact** | Notify: [teams to notify when this changes] |
| **Review Cadence** | [Weekly/Monthly/Quarterly/As-needed] |

---

## Table of Contents

1. [Section Title](#1-section-title)
2. [Section Title](#2-section-title)
3. [Section Title](#3-section-title)
4. [Section Title](#4-section-title)
5. [Section Title](#5-section-title)
6. [Additional Sections (Optional)](#6-additional-sections-optional---add-as-needed)

---

## 1. [Section Title]

[Content for section 1. Use this structure as a guide:]

### Subsection 1.1

**Key Points:**
- Bullet point 1
- Bullet point 2
- Bullet point 3

**Industry Context**: [Include relevant research, benchmarks, or best practices. **Bold key statistics** for visibility.]

**What This Means for GFxAI**: [Interpret the research and provide specific, actionable guidance for our product.]

### Subsection 1.2

[Additional content. Use tables for structured data:]

| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| Data 1   | Data 2   | Data 3   |
| Data 4   | Data 5   | Data 6   |

**Example Code Block** (if applicable):
```javascript
// Code example with syntax highlighting
function example() {
  return "Use code blocks for technical examples";
}
```

## 2. [Section Title]

[Content for section 2. Consider these content types:]

### Use Case or Scenario

**Scenario**: [Describe a concrete example or use case]

**Approach**: [How to handle this scenario]

**Expected Outcome**: [What success looks like]

### Framework or Methodology

**Step 1: [Action]**
- Detail 1
- Detail 2
- Detail 3

**Step 2: [Action]**
- Detail 1
- Detail 2
- Detail 3

### Metrics and Benchmarks

| Metric | Industry Benchmark | GFxAI Target | Notes |
|--------|-------------------|--------------|-------|
| Metric 1 | X% | Y% | Context about this metric |
| Metric 2 | X units | Y units | Why we set this target |

## 3. [Section Title]

[Content for section 3. Include comparisons, trade-offs, or decision frameworks:]

### Comparison Table

| Option A | Option B | Option C |
|----------|----------|----------|
| Pro: Benefit 1 | Pro: Benefit 1 | Pro: Benefit 1 |
| Pro: Benefit 2 | Pro: Benefit 2 | Pro: Benefit 2 |
| Con: Drawback 1 | Con: Drawback 1 | Con: Drawback 1 |
| **Recommended for:** Use case A | **Recommended for:** Use case B | **Recommended for:** Use case C |

### Decision Criteria

**When to choose Option A:**
1. Condition 1
2. Condition 2
3. Condition 3

**When to choose Option B:**
1. Condition 1
2. Condition 2
3. Condition 3

## 4. [Section Title]

[Content for section 4. Include best practices, anti-patterns, or implementation guidance:]

### Best Practices

**DO:**
- ✅ Best practice 1 with explanation
- ✅ Best practice 2 with explanation
- ✅ Best practice 3 with explanation

**DON'T:**
- ❌ Anti-pattern 1 with explanation of why it's bad
- ❌ Anti-pattern 2 with explanation of why it's bad
- ❌ Anti-pattern 3 with explanation of why it's bad

### Implementation Checklist

When implementing [this topic], follow this checklist:

- [ ] **Step 1**: [Action item with brief explanation]
- [ ] **Step 2**: [Action item with brief explanation]
- [ ] **Step 3**: [Action item with brief explanation]
- [ ] **Step 4**: [Action item with brief explanation]
- [ ] **Step 5**: [Action item with brief explanation]

## 5. [Section Title]

[Content for section 5. Include success metrics, monitoring, or continuous improvement:]

### Success Metrics

**Primary Metrics:**

| Metric | Definition | Target | Measurement Method |
|--------|-----------|--------|-------------------|
| Metric 1 | What it measures | Target value | How to track it |
| Metric 2 | What it measures | Target value | How to track it |

**Secondary Metrics:**

| Metric | Definition | Target | Measurement Method |
|--------|-----------|--------|-------------------|
| Metric 3 | What it measures | Target value | How to track it |
| Metric 4 | What it measures | Target value | How to track it |

### Monitoring and Alerts

**Key Indicators to Watch:**
- **Indicator 1**: What to watch, what threshold triggers concern
- **Indicator 2**: What to watch, what threshold triggers concern
- **Indicator 3**: What to watch, what threshold triggers concern

### Continuous Improvement

**Regular Review Activities:**
1. **[Frequency]**: [What to review and why]
2. **[Frequency]**: [What to review and why]
3. **[Frequency]**: [What to review and why]

**Experiment Ideas:**
- [ ] **Hypothesis 1**: [If we change X, then Y will improve because Z]
- [ ] **Hypothesis 2**: [If we change X, then Y will improve because Z]
- [ ] **Hypothesis 3**: [If we change X, then Y will improve because Z]

---

## 6. Additional Sections (Optional - Add as Needed)

### Common Pitfalls and Troubleshooting

| Problem | Symptoms | Root Cause | Solution |
|---------|----------|------------|----------|
| Issue 1 | How it manifests | Why it happens | How to fix |
| Issue 2 | How it manifests | Why it happens | How to fix |

### Resources and References

**Internal Resources:**
- [Link to internal doc](path/to/doc.md) - Brief description
- [Link to internal tool](path/to/tool.md) - Brief description

**External Resources:**
- [External article title](https://url.com) - Brief description
- [Industry research](https://url.com) - Brief description

### Glossary

| Term | Definition |
|------|------------|
| **Term 1** | Clear, concise definition |
| **Term 2** | Clear, concise definition |
| **Acronym** | What it stands for and what it means |

### FAQ

**Q: [Common question]?**
A: [Clear, concise answer with context]

**Q: [Common question]?**
A: [Clear, concise answer with context]

**Q: [Common question]?**
A: [Clear, concise answer with context]

---

## Appendices *(if applicable — Lightweight tier may omit)*

### Appendix A: [Topic]
[Supplementary content]

### Appendix B: Document Provenance *(if applicable)*
[Include when doc was generated from/merged from other sources]

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | [Date] | [Author] | Initial creation |

---

> **See also:**
> - [parent-doc.md](../path/to/parent.md) - Brief description of what this doc contains
> - [related-doc-1.md](path/to/related-1.md) - Brief description of relevance
> - [related-doc-2.md](path/to/related-2.md) - Brief description of relevance
> - [related-doc-3.md](path/to/related-3.md) - Brief description of relevance

---

> **Template Version:** 1.0
> **Template Created:** 2026-03-11
> **Template Type:** General Reference / Supplemental Document
> **See Also:** [operational_guide_template.md](operational_guide_template.md), [technical_reference_template.md](technical_reference_template.md)

<!-- ═══════════════════════════════════════════════════════════════
     GOVERNANCE COMMENTS — Guidance for template users (strip from final docs)
     ═══════════════════════════════════════════════════════════════ -->

<!-- LINE BUDGET / LENGTH TARGETS
     Lightweight: 200-400 lines
     Standard: 400-800 lines
     Heavyweight: 800-1200 lines
     These are guidelines, not hard limits. Prioritize completeness over brevity. -->

<!-- CONTENT RULES
     This template is for general reference documents, research summaries, process
     documentation, and supplemental guides that don't fit the PRD, TDD, Tech Reference,
     Operational Guide, or README categories.
     - DO include: research findings, best practices, frameworks, decision criteria,
       benchmarks, comparisons, implementation guidance
     - DON'T include: step-by-step setup procedures (use Operational Guide),
       API specifications (use Tech Reference), product requirements (use PRD),
       technical designs (use TDD) -->

<!-- FILE NAMING CONVENTION
     Pattern: [topic-name]-reference.md (kebab-case)
     Examples: pricing-strategy-reference.md, security-audit-reference.md,
               performance-benchmarks-reference.md -->

<!-- CALLOUT CONVENTIONS
     Use these standardized callout formats throughout the document:
     > **Note:** General information or helpful context
     > **Important:** Key information that affects usage or decisions
     > **CRITICAL:** Must-read information — ignoring this causes failures
     > **Tip:** Optional but recommended best practice -->

<!-- ANTI-PATTERNS
     Common mistakes when writing supplemental/general reference documents:
     - Turning a reference doc into a step-by-step guide (use Operational Guide instead)
     - Including API specs or code-level details (use Tech Reference instead)
     - Writing requirements as prose instead of using a PRD
     - Duplicating content that already exists in another doc — link, don't copy
     - Leaving placeholder sections empty without removing or marking them -->

<!-- ZERO CONTENT LOSS RULE
     When normalizing an existing document to this template, ALL original content
     must be preserved — relocated to the appropriate section, not dropped.
     If content doesn't fit any section, place it in Appendices with a note
     explaining why it was relocated. Content may be reformatted but never deleted. -->
