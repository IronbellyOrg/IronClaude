---
id: "GFXAI-[GUIDE-NAME]"
title: "[Human Readable Guide Title]"
description: "[One-sentence summary of what this guide covers and who it is for]"
version: "1.0"
status: "📝 Template"
type: "📘 Operational Guide"
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
- [path/to/related-guide-1.md]
- [path/to/related-guide-2.md]
tags:
- operational-guide
- tag2
- tag3
template_schema_doc: ".claude/templates/documents/operational_guide_template.md"
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

# [Guide Title]

> **WHAT:** [One sentence describing what this guide covers — e.g., "Step-by-step installation of the GFxAI platform on a Docker host."]
> **WHY:** [One sentence explaining why this guide exists — e.g., "Ensures consistent, repeatable deployments across environments."]
> **HOW TO USE:** [One sentence on who should use it and when — e.g., "Follow this guide when setting up a new environment or re-deploying from scratch."]

### Document Lifecycle Position

**Standalone document** — not part of the PRD → TDD → Tech Ref lifecycle.

### Tiered Usage

| Tier | When to Use | Sections Required |
|------|-------------|-------------------|
| **Lightweight** | Single-phase guide, <10 steps, single system | Overview, Prerequisites, Phase(s), Verification, Troubleshooting, Quick Reference |
| **Standard** | Multi-phase guide, most operational guides | All sections |
| **Heavyweight** | Cross-system deployment, 5+ phases, complex verification | All sections, plus additional phases as needed |

---

## Document Information

| Field | Value |
|-------|-------|
| **Guide Name** | [Guide Title] |
| **Guide Type** | [Installation / Setup / Deployment / Operations / CI/CD] |
| **Target Environment** | [e.g., Docker Host, Windows VM, Kubernetes Cluster] |
| **Maintained By** | [Team or person] |
| **Last Verified Against System** | [Date and environment version] |
| **Prerequisites Guide** | [Link to prerequisite guide, if any] |
| **Next Guide** | [Link to follow-up guide, if any] |

---

## Completeness Status

**Completeness Checklist:**
- [ ] Section 1: Overview — **Status**
- [ ] Section 2: Prerequisites — **Status**
- [ ] Section 3-5: Phases — **Status**
- [ ] Section 6: Verification — **Status**
- [ ] Section 7: Troubleshooting — **Status**
- [ ] Section 8: Maintenance & Operations — **Status**
- [ ] Section 9: Quick Reference — **Status**
- [ ] Section 10: Next Steps — **Status**
- [ ] All links verified — **Status**
- [ ] Reviewed by [team] — **Status**

**Contract Table:**

| Element | Details |
|---------|---------|
| **Dependencies** | [Docs/systems this guide depends on] |
| **Upstream** | Feeds from: [what provides input to this guide] |
| **Downstream** | Feeds to: [what consumes this guide] |
| **Change Impact** | Notify: [teams to notify when this changes] |
| **Review Cadence** | [Quarterly / Monthly / As-needed] |

---

## Table of Contents

1. [Overview](#1-overview)
2. [Prerequisites](#2-prerequisites)
3. [Phase 1: [Phase Name]](#3-phase-1-phase-name)
4. [Phase 2: [Phase Name]](#4-phase-2-phase-name)
5. [Phase 3: [Phase Name]](#5-phase-3-phase-name)
6. [Verification](#6-verification)
7. [Troubleshooting](#7-troubleshooting)
8. [Maintenance & Operations](#8-maintenance--operations)
9. [Quick Reference](#9-quick-reference)
10. [Next Steps](#10-next-steps)

---

## 1. Overview

> *Provide a high-level summary of what this guide accomplishes. Include an architecture diagram if the guide involves multiple systems or services.*

### 1.1 Purpose

[Brief description of the guide's purpose and scope — what will be set up, deployed, or configured by the end.]

### 1.2 Architecture Overview *(if applicable)*

[ASCII diagram showing the systems, services, or components involved and how they relate.]

```
┌─────────────────────────────┐
│  [Component A]              │
│  ├── [Sub-component]        │
│  └── [Sub-component]        │
├─────────────────────────────┤
│  [Component B]              │
│  └── [Sub-component]        │
└─────────────────────────────┘
```

### 1.3 What You Will Accomplish

By the end of this guide you will have:
- [Outcome 1]
- [Outcome 2]
- [Outcome 3]

---

## 2. Prerequisites

> *Everything that must be in place before starting. The reader should verify ALL items in this section before proceeding to Phase 1.*

### 2.1 Host Specifications

| Requirement | Minimum | Recommended | Actual/Verified |
|-------------|---------|-------------|-----------------|
| OS | [e.g., Ubuntu 22.04+] | [e.g., Ubuntu 24.04] | [Fill in during setup] |
| CPU | [e.g., 4 cores] | [e.g., 8 cores] | |
| RAM | [e.g., 8 GB] | [e.g., 16 GB] | |
| Disk | [e.g., 50 GB] | [e.g., 100 GB SSD] | |
| Network | [e.g., Internet access] | [e.g., Static IP] | |

### 2.2 Software Requirements

| Software | Version | Required/Optional | Installation Notes |
|----------|---------|-------------------|-------------------|
| [e.g., Docker] | [e.g., 24.0+] | Required | [Link or install command] |
| [e.g., Docker Compose] | [e.g., v2.20+] | Required | [Included with Docker Desktop] |
| [e.g., Git] | [e.g., 2.40+] | Required | |

### 2.3 Network Requirements *(if applicable)*

| Port | Protocol | Direction | Purpose |
|------|----------|-----------|---------|
| [e.g., 8102] | TCP | Inbound | [e.g., Backend API] |
| [e.g., 3501] | TCP | Inbound | [e.g., Frontend] |

### 2.4 Pre-Flight Checklist

> **Verify all items before proceeding.**

- [ ] Host meets minimum specifications (Section 2.1)
- [ ] All required software installed (Section 2.2)
- [ ] Network ports available and firewall rules configured (Section 2.3)
- [ ] [Any other prerequisite — e.g., "Access credentials obtained"]
- [ ] [Any other prerequisite — e.g., "Repository access confirmed"]

---

## 3. Phase 1: [Phase Name]

> *[Brief description of what this phase accomplishes and why it must come first.]*

### Step 1.1: [Step Name]

[Description of what this step does.]

```bash
# [Command description]
[command here]
```

> **Expected Output:**
> ```
> [What the user should see if the command succeeds]
> ```

### Step 1.2: [Step Name]

[Description of what this step does.]

```bash
[command here]
```

> **Note:** [Any important caveats or tips for this step.]

### Step 1.3: Verify Phase 1 *(inline verification checkpoint)*

[Verification command or check to confirm Phase 1 completed successfully.]

```bash
# Verify [what you are checking]
[verification command]
```

**Expected result:** [What success looks like.]

---

## 4. Phase 2: [Phase Name]

> *[Brief description of what this phase accomplishes.]*

### Step 2.1: [Step Name]

[Content follows same patterns as Phase 1 — steps, commands, expected output, notes.]

<!--
TEMPLATE GUIDANCE — Phase/Step Patterns:
- Use "Step X.Y:" numbering within each phase (e.g., Step 2.1, Step 2.2)
- Include inline verification checkpoints at the end of each phase
- Use blockquote callouts for important notes:
  > **Note:** Informational context
  > **Important:** Something the user must be aware of
  > **CRITICAL:** Something that will cause failure if ignored
  > **Tip:** Helpful shortcut or best practice
- Include "Expected Output" blocks after commands where the output matters
- When multiple approaches exist, use the Option pattern:

  **Option A: [Approach Name]** *(Recommended)*
  ```bash
  [commands]
  ```

  **Option B: [Alternative Approach Name]**
  ```bash
  [commands]
  ```
-->

---

## 5. Phase 3: [Phase Name]

> *[Brief description of what this phase accomplishes.]*

[Content follows same patterns as previous phases.]

<!--
TEMPLATE GUIDANCE — Adding More Phases:
- Add as many Phase sections as needed (Phase 4, Phase 5, etc.)
- Update the Table of Contents numbering accordingly
- Each phase should build on the previous one
- Keep phases focused — one logical grouping of steps per phase
- Name phases descriptively (e.g., "Phase 3: Database Initialization" not "Phase 3: Step 3")
-->

---

## 6. Verification

> *Comprehensive verification that the entire setup/deployment/configuration is working correctly. This goes beyond the inline checkpoint verifications within each phase.*

### 6.1 Health Checks

[Commands or procedures to verify all services/components are healthy.]

| Service/Component | Check Command | Expected Status |
|-------------------|---------------|-----------------|
| [e.g., Backend API] | `[e.g., curl http://localhost:8102/health]` | `[e.g., {"status": "healthy"}]` |
| [e.g., Frontend] | `[e.g., curl -s -o /dev/null -w "%{http_code}" http://localhost:3501]` | `[e.g., 200]` |

### 6.2 End-to-End Validation

[Steps to verify the system works as an integrated whole, not just individual components.]

1. [Validation step 1]
2. [Validation step 2]
3. [Validation step 3]

### 6.3 All-Green Checklist

- [ ] [Component/service 1] is running and responding
- [ ] [Component/service 2] is running and responding
- [ ] [Integration point] is functional
- [ ] [End-to-end workflow] completes successfully

---

## 7. Troubleshooting

> *Common issues encountered during setup/deployment and their solutions. Organize by category for easy scanning.*

### 7.1 [Category Name] Issues

| Symptom | Cause | Solution |
|---------|-------|----------|
| [What the user sees] | [Why it happens] | [How to fix it] |
| [What the user sees] | [Why it happens] | [How to fix it] |

### 7.2 [Category Name] Issues

| Symptom | Cause | Solution |
|---------|-------|----------|
| [What the user sees] | [Why it happens] | [How to fix it] |

### 7.3 Diagnostic Commands

```bash
# [Description of what this checks]
[diagnostic command]

# [Description of what this checks]
[diagnostic command]
```

### 7.4 Reset / Clean Start *(if applicable)*

> **CRITICAL:** This will destroy existing data. Only use when a fresh start is needed.

```bash
# [Commands to reset the environment to a clean state]
[reset commands]
```

---

## 8. Maintenance & Operations *(if applicable)*

> *Ongoing operational procedures after initial setup is complete. Skip this section for one-time setup guides.*

### 8.1 Daily Operations

| Task | Command | Frequency |
|------|---------|-----------|
| [e.g., Check service health] | `[command]` | Daily |
| [e.g., Review logs] | `[command]` | Daily |

### 8.2 Backup Procedures

[Backup commands and schedules.]

### 8.3 Update Procedures

[How to apply updates, patches, or configuration changes.]

### 8.4 Snapshot / Rollback Strategy *(if applicable)*

[How to create snapshots before changes, and how to roll back if needed.]

---

## 9. Quick Reference

> *Cheat sheet for daily use after setup is complete. This section should be self-contained — a user familiar with the system should be able to use it without reading the full guide.*

### 9.1 Service URLs / Endpoints

| Service | URL | Notes |
|---------|-----|-------|
| [e.g., Backend API] | `http://<HOST>:8102` | |
| [e.g., Frontend] | `http://<HOST>:3501` | |

### 9.2 Key Paths

| Path | Purpose |
|------|---------|
| [e.g., `/opt/gfxai/`] | [e.g., Installation root] |
| [e.g., `.env.network`] | [e.g., Network configuration] |

### 9.3 Common Commands

```bash
# [Category: e.g., Service Management]
[command]    # [description]
[command]    # [description]

# [Category: e.g., Logs]
[command]    # [description]
```

### 9.4 Configuration Files

| File | Purpose | Key Settings |
|------|---------|-------------|
| [e.g., `.env`] | [e.g., Environment variables] | [e.g., DATABASE_URL, REDIS_URL] |
| [e.g., `docker-compose.yml`] | [e.g., Service definitions] | [e.g., Ports, volumes] |

### 9.5 Default Credentials *(if applicable)*

> **Important:** Change all default credentials before production use.

| Service | Username | Default Password | Notes |
|---------|----------|-----------------|-------|
| [e.g., PostgreSQL] | [e.g., gfxai] | [e.g., See .env] | |

---

## 10. Next Steps

| Priority | Guide | Description |
|----------|-------|-------------|
| 1 | [Link to next guide] | [What it covers] |
| 2 | [Link to related guide] | [What it covers] |
| 3 | [Link to related guide] | [What it covers] |

---

## Appendix *(if applicable)*

### A. [Appendix Topic]

[Supplementary content that supports the guide but is not part of the main procedural flow — e.g., source file references, software version matrices, alternative configurations.]

### B. [Appendix Topic]

[Additional supplementary content.]

### C. Document Provenance *(if applicable)*

> *Include this section when the guide was generated from, merged from, or synthesized from other source documents. This preserves the creation lineage of the guide — information that does not belong in the YAML frontmatter or Document History table.*

| Property | Value |
|----------|-------|
| Generated From | [Method of creation — e.g., "Multi-agent comparison analysis", "Manual consolidation"] |
| Base Document | [Primary source document, if any] |
| Merged Content | [Additional documents merged into this guide, if any] |
| Analysis Source | [Analysis or recommendation document used, if any] |
| Validation | [How the content was validated — e.g., "Adversarial review", "Peer review", "Walkthrough verification"] |
| Source Files Analyzed | [Number or list of source files analyzed] |

<!--
TEMPLATE GUIDANCE — Document Provenance:
- Include this section when the guide was created from other documents (merged, synthesized, analyzed)
- Do NOT include if the guide was written from scratch with no source documents
- This captures metadata about HOW the guide was created — distinct from:
  - YAML frontmatter (which captures identity and classification)
  - Document History (which captures version-over-version changes)
  - Provenance captures the creation lineage and source materials
- When normalizing an existing guide to this template, check the original for
  provenance metadata (author notes, source references, generation info) and
  relocate it here. Do NOT silently drop this information.
-->

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | [YYYY-MM-DD] | [Author] | Initial guide created |
| [X.Y] | [YYYY-MM-DD] | [Author] | [Summary of what changed and why] |

---

<!--
================================================================================
TEMPLATE USAGE INSTRUCTIONS (Remove this block when creating a guide from this template)
================================================================================

## How to Use This Template

1. **Copy this file** and rename it following the guide naming convention (kebab-case):
   - Numbered guides: `nn-guide-name-guide.md` (e.g., `04-new-service-setup-guide.md`)
   - Standalone guides: `name-guide.md` or `name-name-guide.md` (e.g., `monitoring-operations-guide.md`)

2. **Fill in the YAML frontmatter** with actual values:
   - `id`: Use `"GFXAI-[DESCRIPTIVE-NAME]"` format
   - `title`: Human-readable guide title
   - `status`: Start with `"🟡 Draft"`, update to `"🟢 Published"` after review
   - `type`: Keep as `"📘 Operational Guide"`
   - `template_schema_doc`: Set to `".claude/templates/documents/operational_guide_template.md"`
   - Fill in all dates, tags, and related_docs

3. **Adapt the section structure** to fit your guide:
   - Sections 1-2 (Overview, Prerequisites): Always include
   - Sections 3-5 (Phases): Add or remove phases as needed. Renumber TOC accordingly.
   - Section 6 (Verification): Always include
   - Section 7 (Troubleshooting): Always include
   - Section 8 (Maintenance): Include for systems that require ongoing operations.
     Omit for one-time setup guides.
   - Section 9 (Quick Reference): Always include
   - Section 10 (Next Steps): Include when this guide is part of a sequence
   - Appendix: Include when supplementary content exists
   - Appendix C (Document Provenance): Include when the guide was generated from,
     merged from, or synthesized from other source documents

4. **Phase naming convention**: Use descriptive phase names:
   - GOOD: "Phase 1: Repository Setup", "Phase 3: Docker Deployment"
   - BAD: "Phase 1: Step 1", "Phase 3: Continue"
   - Alternative: Use "Part" instead of "Phase" if it fits the content better

5. **Step numbering**: Use `Step X.Y` format within phases (e.g., Step 1.1, Step 1.2).
   For deeply nested procedures, extend to `Step X.Y.Z` (e.g., Step 1.5.1).

6. **Callout conventions** (use throughout the guide):
   > **Note:** Informational context that is helpful but not critical
   > **Important:** Something the user must be aware of to avoid issues
   > **CRITICAL:** Something that will cause failure or data loss if ignored
   > **Tip:** Helpful shortcut, best practice, or time-saving suggestion

7. **Content rules**:
   - Use tables for structured data (specs, ports, commands, troubleshooting)
   - Use ASCII diagrams for architecture and data flow
   - Include "Expected Output" blocks after commands where output matters
   - Use code blocks with language tags (```bash, ```powershell, ```yaml, etc.)
   - Use the Option A/B/C pattern when multiple approaches exist
   - Include inline verification checkpoints at the end of each phase
   - Keep the Quick Reference section self-contained (usable without reading the full guide)

8. **Remove all template guidance** (HTML comments and placeholder text) from your
   final guide. Keep only actual content.

9. **Zero content loss during normalization**: When normalizing an existing guide to
   this template, ALL original content must be preserved. Content may be relocated
   (e.g., metadata → frontmatter, version history → Document History table,
   provenance info → Appendix C) but NEVER silently dropped. Specifically:
   - Version/change history → Document History table rows
   - Document provenance metadata (author, source docs, generation method,
     validation method) → Appendix C: Document Provenance
   - Audit status or verification status → Document Information table row
   - If content does not fit any template section, create a new Appendix subsection

================================================================================
-->

<!--
LINE BUDGET — Target line counts per tier:
- Lightweight (single-phase, <10 steps): 200–400 lines
- Standard (multi-phase, most guides): 400–800 lines
- Heavyweight (cross-system deployment, 5+ phases): 800–1200 lines

These are guidelines, not hard limits. Prioritize completeness over brevity.
-->

<!--
CONTENT RULES:
- Use tables for structured data (specs, ports, commands, troubleshooting)
- Use ASCII diagrams for architecture and data flow
- Include "Expected Output" blocks after commands where output matters
- Use code blocks with language tags (bash, powershell, yaml, etc.)
- Use the Option A/B/C pattern when multiple approaches exist
- Include inline verification checkpoints at the end of each phase
- Keep the Quick Reference section self-contained (usable without reading the full guide)
- Operational guides define HOW to deploy/set up — not WHAT to build (PRD) or HOW to design (TDD)
-->

<!--
FILE NAMING CONVENTION:
Operational guide files use kebab-case:
- Numbered guides: nn-guide-name-guide.md (e.g., 04-new-service-setup-guide.md)
- Standalone guides: name-guide.md or name-name-guide.md (e.g., monitoring-operations-guide.md)
- Always lowercase, hyphens as separators
-->

<!--
CALLOUT CONVENTIONS:
Use these standardized callout formats throughout the document:
  > **Note:** Informational context that is helpful but not critical
  > **Important:** Something the user must be aware of to avoid issues
  > **CRITICAL:** Something that will cause failure or data loss if ignored
  > **Tip:** Helpful shortcut, best practice, or time-saving suggestion
-->

> **See also:**
> - [Technical Reference Template](technical_reference_template.md) — For documenting implemented features and systems
> - [Supplemental Doc Template](supplemental_doc_template.md) — For process standards and reference documents
> - [PRD Template](prd_template.md) — For product requirements and feature specifications

---

> **Template Version:** 1.0
> **Template Created:** 2026-03-08
> **Template Updated:** 2026-03-11
> **Template Type:** Operational Guide — for installation guides, setup guides, deployment guides, CI/CD pipeline docs, and operational runbooks
> **Based On:** Analysis of existing project templates (technical_reference_template.md, supplemental_doc_template.md, prd_template.md) and structure analysis of 4 existing operational guides (01-gfxai-installation-guide.md, 02-unreal-gameframeproject-setup-guide.md, 03-pixel-streaming-unified-setup-guide.md, CICD-PIPELINE-AND-DEPLOYMENT-PROCESS.md)
