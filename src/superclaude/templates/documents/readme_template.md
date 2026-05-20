---
id: "[PROJECT-OR-MODULE-ID]-README"
title: "[Project/Module Name] - README"
description: "README file for [project/module name] providing overview, quick start, usage, and navigation for developers and contributors"
version: "1.0"
status: "🟡 Draft"
type: "📖 README"
priority: "🔼 High"
created_date: "YYYY-MM-DD"
updated_date: "YYYY-MM-DD"
assigned_to: "[engineering-team]"
autogen: false
autogen_method: ""
coordinator: "[tech-lead]"
parent_doc: ""
depends_on:
- "[list dependent documents]"
related_docs:
- "[list related documents]"
tags:
- readme
- "[project-name]"
- documentation
- onboarding
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
# --- Document Information (in frontmatter for external-facing READMEs — GitHub does not render YAML frontmatter) ---
document_information:
  document_name: "[Project/Module Name] README"
  document_type: "README"
  maintained_by: "[team or person]"
  last_verified: "[YYYY-MM-DD against commit hash or version]"
# --- Completeness Status (in frontmatter for external-facing READMEs) ---
completeness_status:
  checklist:
    - "Section 1 (About): [Draft/Complete/N-A]"
    - "Section 2 (Features): [Draft/Complete/N-A]"
    - "Section 4 (Quick Start): [Draft/Complete/N-A]"
    - "Section 5 (Usage): [Draft/Complete/N-A]"
    - "All links verified: [Yes/No]"
    - "Reviewed by [team]: [Yes/No]"
# --- Contract Table (in frontmatter for external-facing READMEs) ---
contract_table:
  dependencies: "[Docs/systems this README depends on]"
  upstream: "[What provides input — e.g., PRD, TDD, architecture docs]"
  downstream: "[What consumes this — e.g., onboarding process, contributor workflow]"
  change_impact: "[Teams to notify when this README changes]"
  review_cadence: "[Quarterly / Monthly / As-needed]"
---

# [Project Name]

> **WHAT:** A README template for project or module entry-point documentation — covers overview, quick start, usage, and navigation.
> **WHY:** Provides a standardized, research-backed structure so every README answers "What is this? How do I use it? Where do I go next?" consistently.
> **HOW TO USE:** Engineering teams and contributors use this template when creating or updating a README for any project, module, or package.

### Document Lifecycle Position

**Standalone document** — not part of the PRD → TDD → Tech Ref lifecycle.

### Tiered Usage

| Tier | When to Use | Sections Required | Target Length |
|------|-------------|-------------------|---------------|
| **Lightweight** | Small library, utility, single-purpose module | 1, 2, 5, 6, 13 | 50–150 lines |
| **Standard** | Most applications and frameworks | All numbered sections; skip sections marked *(if applicable)* | 150–400 lines |
| **Heavyweight** | Platform, monorepo, multi-service system | All sections fully completed | 200–500 lines |

<!-- README-SPECIFIC GUIDANCE (retained from original orientation block):

**Audience:** The README serves three audiences simultaneously:
| Audience | Primary Question | Key Sections |
|----------|-----------------|--------------|
| **New users** | "What is this and should I use it?" | Description, Features, Quick Start |
| **New contributors** | "How do I set up and contribute?" | Development Setup, Project Structure, Contributing |
| **Returning contributors** | "Where is X?" | TOC, Project Structure, Documentation Links |

**Key Principle:** As a project grows, the README becomes more *navigational* and less *instructional*. Small projects explain everything inline; large projects orient the reader and link to deeper docs. The README is an entry point, not exhaustive documentation.

**Research Basis:** This template synthesizes findings from Prana et al. (2018) — an empirical study of 4,226 README sections across 393 GitHub repositories — GitHub's official README guidance, Make a README (makeareadme.com), and patterns from top open-source projects (React, FastAPI, Tailwind CSS, Next.js). See `.dev/wizard-research/readme-template-research.md` for full research notes.
-->

---

<!-- TEMPLATE INSTRUCTIONS (delete this block when using):

1. Replace all [bracketed placeholders] with actual content
2. Delete any section not relevant to your tier
3. Remove all HTML comments (template instructions) from the final document
4. The final README should contain NO template instructions, placeholders, or meta-commentary
5. Keep the frontmatter — it is stripped when rendering but used for document management

-->

[Logo or project banner image — optional but recommended for Standard/Heavyweight tier]

[![Build Status](https://img.shields.io/github/actions/workflow/status/org/repo/ci.yml?branch=main)](link-to-ci)
[![Version](https://img.shields.io/npm/v/package-name)](link-to-releases)
[![License](https://img.shields.io/github/license/org/repo)](LICENSE)
[![Coverage](https://img.shields.io/codecov/c/github/org/repo)](link-to-coverage)

<!-- BADGE GUIDELINES:
- 4–6 badges maximum for most projects (8–10 for major platforms)
- Only include badges that convey actionable information
- All badges must be dynamic (auto-updating), not static
- Link each badge to its source (CI badge → CI dashboard, etc.)
- Remove any badge that is broken or not yet configured
- Suggested order: Build → Version → License → Coverage → Downloads
-->

[One-line tagline — what the project does and why it matters, in a single sentence.]

---

## Table of Contents

<!-- Include TOC only when README exceeds ~100 lines. For Lightweight tier, omit this section. -->

1. [About](#1-about)
2. [Features](#2-features)
3. [Prerequisites](#3-prerequisites)
4. [Quick Start](#4-quick-start)
5. [Usage](#5-usage)
6. [Configuration](#6-configuration)
7. [Project Structure](#7-project-structure)
8. [Architecture](#8-architecture)
9. [Development Setup](#9-development-setup)
10. [Testing](#10-testing)
11. [Deployment](#11-deployment)
12. [Documentation](#12-documentation)
13. [Contributing](#13-contributing)
14. [Roadmap](#14-roadmap)
15. [FAQ / Troubleshooting](#15-faq--troubleshooting)
16. [License](#16-license)
17. [Acknowledgments](#17-acknowledgments)

---

## 1. About

<!-- 2–4 sentences maximum. Answer three questions: What is this? Who is it for? Why should I care?
Lead with the value proposition, not the technology.
Write for someone who just found this project via search and has never heard of it.

GOOD: "GameFrame AI enables game developers to create professional games by describing features in plain English, powered by specialized AI agents."
BAD: "This is a Next.js 14 application using Zustand, FastAPI, LangChain, and PostgreSQL that..." -->

[2–4 sentence description. What it does, who it's for, why it matters.]

<!-- For Heavyweight/platform projects, include a quick-reference metadata block:
> **Status:** [Production / Beta / Alpha / Experimental]
> **Requires:** [Key runtime dependencies, e.g., "Node.js 18+, PostgreSQL 15+"]
> **License:** [License name]
> **Docs:** [Link to documentation site]
-->

---

## 2. Features

<!-- Bullet list of key capabilities. 5–10 items for most projects.
Each item: one line, plain language, user-focused (what can I do?), not implementation-focused (how does it work?).

GOOD: "Real-time game preview via Pixel Streaming — see changes instantly in the browser"
BAD: "Uses WebRTC-based UE5.6 Pixel Streaming Frontend library with bidirectional input handling" -->

- [Feature 1 — one-line description of user-facing capability]
- [Feature 2]
- [Feature 3]
- [Feature 4]
- [Feature 5]

---

## 3. Prerequisites

<!-- List what must be installed BEFORE the Quick Start steps.
Include exact version requirements. Link to installation guides for non-obvious dependencies.
Omit for Lightweight tier if prerequisites are obvious (e.g., a published npm package). -->

- [Runtime] v[X.Y]+ — [link to install guide]
- [Database] v[X.Y]+ — [link to install guide]
- [Other dependency] — [link or install command]

---

## 4. Quick Start

<!-- The single most important section. Show the shortest path from zero to working.
Rules:
1. Maximum 5 steps for the "happy path"
2. Every command must be copy-pasteable (no "replace X with your value" if avoidable)
3. Show expected output after the final step
4. Platform-specific instructions go in collapsible sections or separate docs
5. Do NOT include configuration, customization, or edge cases — that's for Usage/Configuration sections -->

```bash
# 1. Clone the repository
git clone https://github.com/org/repo.git
cd repo

# 2. Install dependencies
[package manager install command]

# 3. Configure environment
cp .env.example .env
# Edit .env with your settings

# 4. Start the application
[start command]
```

The application will be available at `http://localhost:[PORT]`.

<!-- If the project has multiple entry points (frontend + backend), show the simplest unified start command.
Link to Development Setup (Section 9) for the full multi-service setup. -->

---

## 5. Usage

<!-- Show 1–3 key usage examples. Start with the simplest possible example.
Rules:
1. Use real, runnable code (not pseudocode)
2. Include expected output alongside code
3. Progress from basic to advanced
4. Link to full documentation for comprehensive usage guides
5. For Lightweight tier, this is the primary instructional section — be thorough here -->

### Basic Example

```[language]
[Minimal working example with expected output]
```

### [Additional Example — if applicable]

```[language]
[More advanced example]
```

For comprehensive usage guides, see the [Documentation](#12-documentation).

---

## 6. Configuration

<!-- *(if applicable)* — Omit for Lightweight tier.
Summarize key configuration options. Do NOT reproduce full config files.
Use a table for environment variables / key settings.
Link to full configuration reference docs. -->

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `[VAR_NAME]` | Yes | — | [What it configures] |
| `[VAR_NAME]` | No | `[default]` | [What it configures] |

See `[.env.example or config reference path]` for the complete configuration reference.

---

## 7. Project Structure

<!-- Show the top 2–3 levels of nesting only. One-line description per directory.
Focus on directories a developer needs to understand to navigate the codebase.
For Heavyweight/monorepo projects, link each major directory to its own README.

Do NOT include:
- Individual files (except key entry points)
- node_modules, .git, build output, or generated directories
- File counts or size statistics (they become stale) -->

```
[project-root]/
├── [dir]/                  # [One-line purpose]
│   ├── [subdir]/           # [One-line purpose]
│   └── [subdir]/           # [One-line purpose]
├── [dir]/                  # [One-line purpose]
├── [dir]/                  # [One-line purpose]
├── [config-file]           # [One-line purpose]
└── [config-file]           # [One-line purpose]
```

<!-- For monorepos, add a navigation guide:
### Where Do I Go For...?
| I want to... | Go to |
|-------------|-------|
| Work on the frontend | `frontend/` — [link to frontend README] |
| Work on the API | `backend/` — [link to backend README] |
| Deploy the platform | `infrastructure/` — [link to deployment docs] |
-->

---

## 8. Architecture

<!-- *(if applicable)* — Include for Standard and Heavyweight tier.
Provide a high-level overview only — 1 diagram + 1–2 paragraphs.
Use ASCII diagrams for version-control-friendly rendering.
Link to Technical Reference or TDD for architectural deep dives.

Do NOT reproduce detailed architecture docs here. The README provides orientation, not specification. -->

```
[High-level architecture diagram — ASCII art, Mermaid, or link to image]
```

[1–2 paragraphs explaining the key architectural decisions and how components interact.]

For detailed architecture documentation, see [link to Technical Reference or architecture docs].

---

## 9. Development Setup

<!-- *(if applicable)* — Omit for Lightweight tier. For Standard/Heavyweight, this expands on Quick Start with the full contributor setup.
Include:
- How to run all services locally
- How to set up the database / seed data
- How to run in development mode (hot reload, debug, etc.)
- IDE recommendations and extensions (optional)
- Common setup issues and solutions

This section answers: "I want to contribute — how do I get a full dev environment running?" -->

### Full Development Environment

```bash
[Step-by-step commands for complete dev setup]
```

### Running Services

| Service | Command | URL |
|---------|---------|-----|
| [Service 1] | `[command]` | `http://localhost:[PORT]` |
| [Service 2] | `[command]` | `http://localhost:[PORT]` |

<!-- For complex setups, link to a dedicated Development Guide:
For detailed setup instructions, see [docs/development-guide.md]. -->

---

## 10. Testing

<!-- Show how to run tests. Include the primary test command and any important variants.
Do NOT reproduce the full testing strategy — link to testing docs.

Essential content:
1. How to run all tests (one command)
2. How to run specific test types (unit, integration, e2e) if applicable
3. Coverage target (if enforced) -->

```bash
# Run all tests
[test command]

# Run specific test types (if applicable)
[unit test command]
[integration test command]
[e2e test command]
```

<!-- Coverage target: [X]% — enforced in CI. -->

For the full testing strategy and tier definitions, see [link to testing docs].

---

## 11. Deployment

<!-- *(if applicable)* — Omit for libraries and Lightweight tier.
Brief summary of how the project is deployed. Link to full deployment documentation.
Do NOT reproduce deployment scripts or detailed CI/CD configuration here. -->

[1–2 sentences describing the deployment approach.]

For deployment instructions, see [link to deployment docs].

---

## 12. Documentation

<!-- Organize links by audience. This section is the "hub" that connects the README to deeper documentation.
For Heavyweight projects, this is one of the most important sections — it prevents readers from getting lost. -->

### For Users
- [User Guide / Getting Started](link)
- [API Reference](link)
- [FAQ / Troubleshooting](#15-faq--troubleshooting)

### For Contributors
- [Contributing Guide](CONTRIBUTING.md)
- [Development Setup](#9-development-setup)
- [Architecture / Technical Reference](link)

### For Operators
- [Deployment Guide](link)
- [Configuration Reference](link)
- [Monitoring / Observability](link)

<!-- For monorepos, include subsystem-specific docs:
### Subsystem Documentation
| Subsystem | README | Technical Reference |
|-----------|--------|-------------------|
| Frontend | [frontend/README.md](link) | [docs/frontend/TECHNICAL_REFERENCE.md](link) |
| Backend | [backend/README.md](link) | [docs/backend/TECHNICAL_REFERENCE.md](link) |
-->

---

## 13. Contributing

<!-- Every README needs this, even for Lightweight tier.
Keep it brief — 3–5 lines maximum. Link to CONTRIBUTING.md for details.
State clearly whether contributions are welcome. -->

Contributions are welcome. Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

<!-- If no CONTRIBUTING.md exists, include the essential process inline:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (see [commit conventions])
4. Open a Pull Request against `[base branch]`
-->

---

## 14. Roadmap

<!-- *(if applicable)* — Omit for Lightweight tier.
Clearly separate current capabilities from planned work.
Use checkboxes or a brief table. Keep it high-level — link to a project board for details.

CRITICAL: Do NOT list planned features as if they already exist.
This is the #1 source of user frustration and eroded trust in READMEs (Prana et al., 2018). -->

- [x] [Completed milestone 1]
- [x] [Completed milestone 2]
- [ ] [Planned milestone 3]
- [ ] [Planned milestone 4]

See the [project board](link) for detailed planning.

---

## 15. FAQ / Troubleshooting

<!-- *(if applicable)* — Include when common issues are known.
Use a Q&A format. Keep entries concise.
Add entries as real users/contributors report issues. -->

<details>
<summary><strong>[Common question or issue]</strong></summary>

[Concise answer or solution with exact commands if applicable.]

</details>

<details>
<summary><strong>[Common question or issue]</strong></summary>

[Concise answer or solution.]

</details>

---

## 16. License

<!-- Always include. One line is sufficient. -->

This project is licensed under the [License Name] License — see the [LICENSE](LICENSE) file for details.

---

## 17. Acknowledgments

<!-- *(if applicable)* — Credit key dependencies, inspirations, or contributors.
Keep it brief. -->

- [Acknowledgment 1]
- [Acknowledgment 2]

---

## Appendices *(if applicable — Lightweight tier may omit)*

### Appendix A: [Topic]
[Supplementary content that supports the README but would break the flow if inline.]

### Appendix B: Document Provenance *(if applicable)*
[Include when README was generated from or merged from other sources.]

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | [Date] | [Author] | Initial creation |

---

> **See also:**
> - [related-doc-1.md](path) — Brief description
> - [related-doc-2.md](path) — Brief description

---

> **Template Version:** 1.0
> **Template Created:** 2026-03-11
> **Template Type:** README — project/module entry-point documentation
> **See Also:** [supplemental_doc_template.md](supplemental_doc_template.md) | [technical_reference_template.md](technical_reference_template.md) | [operational_guide_template.md](operational_guide_template.md)

<!--
LINE BUDGET — Target line counts per tier:
- Lightweight: 50–150 lines
- Standard: 150–400 lines
- Heavyweight: 200–500 lines

If your README exceeds 500 lines, content should be moved to dedicated docs files, not deleted.
The README should become more navigational, not longer.
-->

<!--
CONTENT RULES:
- README is an entry point, not documentation. Link to docs/ for depth.
- Front-load value. The first screenful (~30 lines) must answer: What is this? How do I install it? Where do I get help?
- Show, don't tell. Runnable code examples beat prose explanations. Include expected output.
- Write for the newcomer. Assume the reader has never seen the project. Avoid insider jargon.
- No aspirational content as current. Clearly separate "what exists" from "what's planned." Use the Roadmap section.
- No full configuration reproduction. Summarize key options in a table; link to the source file.
- No architecture deep dives. One diagram + 1–2 paragraphs maximum. Link to Technical Reference for details.
- Keep it current. An outdated README erodes trust more than a short one.

README vs. Other Documents:
| Content Type | Belongs In | NOT In README |
|-------------|-----------|---------------|
| What the project does and why | README (Section 1) | — |
| How to install and get started | README (Sections 4–5) | — |
| Full API reference | Dedicated API docs | README |
| Detailed architecture | Technical Reference | README (brief overview only) |
| Code conventions and standards | CONTRIBUTING.md or CLAUDE.md | README |
| AI agent instructions | CLAUDE.md / AGENTS.md | README |
| Deployment procedures | Deployment docs | README (brief summary only) |
| Detailed configuration | Config reference doc | README (summary table only) |
| Implementation plans / design specs | TDD / PRD | README |
| Changelog | CHANGELOG.md | README |
-->

<!--
FILE NAMING CONVENTION:
Pattern: README.md (always) for root-level project READMEs.
For non-root READMEs (subsystem, module, package): place as README.md inside the relevant directory.
Alternative: [module-name]-README.md only when multiple READMEs must coexist in the same directory.
Examples: README.md, frontend/README.md, frontend/app/wizard/README.md
-->

<!--
CALLOUT CONVENTIONS:
Use these standardized callout formats throughout the document:
  > **Note:** Supplementary information that adds context but is not essential
  > **Important:** Information the reader should be aware of to avoid mistakes
  > **CRITICAL:** Information that, if ignored, will cause failure or data loss
  > **Tip:** Helpful suggestion that improves the reader's experience or workflow
-->

<!--
ADDITIONAL README GUIDANCE:

Monorepo-Specific Rules:
1. Root README is a navigation hub — links to subsystem READMEs
2. Subsystem READMEs follow Lightweight or Standard tier
3. Include a "Where Do I Go For...?" table mapping tasks to directories/docs
4. Do NOT document all subsystems in root README — each owns its own README
5. Quick Start in root README should show the simplest unified start command

Badge Guidelines:
- Maximum 4–6 badges for most projects; 8–10 for major platforms
- Only include badges that convey actionable information
- All badges must be dynamic (auto-updating), not static
- Suggested order: Build Status → Version → License → Coverage → Downloads
- Remove any badge that is broken, not configured, or purely decorative

Anti-Patterns to Avoid:
| Anti-Pattern | Why It's Bad | What to Do Instead |
|-------------|-------------|-------------------|
| Wall of text, no headings | Unscannable; readers leave | Use headers, bullets, code blocks |
| Buried Quick Start | User scrolls past history/architecture | Installation within first screenful |
| Aspirational features as current | Users try features that don't work | Separate Roadmap section with checkboxes |
| README as full documentation | Overwhelms readers; impossible to maintain | Link to docs/ for depth |
| Outdated content | Erodes trust; causes errors | Review cadence; include in PR checklist |
| No usage examples | Users understand theory but not practice | Runnable code examples with expected output |
| Badge wall (15+ badges) | Visual noise; nobody reads them | 4–6 meaningful, dynamic badges |
-->
