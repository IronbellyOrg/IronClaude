---
title: "Rigorflow Framework Directory Structure"
description: "Complete reference map of the Rigorflow framework repository structure, including root files, Claude Code configuration, development tasks, framework core rules, scripts, templates, and test suites. Essential navigation guide for users, developers, and AI agents. Auto-loaded into LLM context via session hooks."
id: "directory-structure-reference"
sidebar_position: 1
created_date: "2025-10-29"
last_updated: "2025-10-29"
version: "5.2"
draft: false
content_status: "Published"
tags:
- directory-structure
- repository-organization
- reference
- navigation
- framework-core
- documentation
- session-context
content_type: "Overview"
target_audience:
- Beginner
- IntermediateUser
- AdvancedUser
- Developer
- SystemArchitect
- AI
- Machine
owner: "framework-team"
autogen: true
autogen_method: "AI"
autogen_source: []
autogen_version: ""
ai_model: "claude-sonnet-4-5-20250929"
model_settings: "{\"temperature\": 0.7, \"max_output_tokens\": 4096, \"top_p\": 0.95, \"top_k\": 40, \"prompt_id\": \"claude_code_default\", \"system_prompt_id\": \"rigorflow_v2.0\", \"stop_sequences\": [], \"frequency_penalty\": 0.0, \"presence_penalty\": 0.0}"
source_references: []
related_links:
- text: "README"
  link: "README.md"
- text: "IB Agent Core"
  link: "~/.claude/rules/core/ib_agent_core.md"
- text: "File Conventions"
  link: "~/.claude/rules/core/file_conventions.md"
related_task_id: []
review_info:
  last_reviewed_by: "framework-team"
  last_review_date: "2025-10-29"
  next_review_date: "2026-04-29"
---

# Rigorflow Framework Directory Structure

**Last Updated:** 2025-10-29
**Version:** 5.2

> **Relocation note:** This document describes the pre-relocation layout; paths were swept `.gfdoc/` -> `.claude/` during the gfdoc retirement.

> **Note:** This file lives at `~/.claude/rules/core/DIRECTORY_STRUCTURE.md` and is auto-loaded into LLM context via session hooks. The former human-reference copy under `docs/` was retired during the relocation; this is now the single canonical location.

---

## Complete Repository Organization

This document provides a complete map of the Rigorflow framework repository structure. Files excluded: workflow artifacts (`.claude/.state`, `.claude/.dev`, example output directories).

---

## Root Level

```
/
├── .claude/                       # Claude Code Configuration
├── .dev/                          # Development & Task Management
├── .claude/                        # Framework Core (rules, scripts, docs)
├── CHANGELOG.md                   # Master changelog (Keep a Changelog format)
├── README.md                      # Project overview and quick start
├── RELEASE_MANIFEST_v2.0.0.md    # Release manifest
└── RELEASE_NOTES_v2.0.0.md       # Release notes
```

---

## .claude/ - Claude Code Configuration

```
.claude/
├── claude.md                      # Project-specific Rigorflow configuration
├── settings.json                  # Claude Code settings
│
├── commands/rf/                   # Rigorflow slash commands
│   ├── README.md                  # Command documentation
│   ├── task.md                    # /rf:task - Execute MDTM tasks
│   ├── taskbuilder.md             # /rf:taskbuilder - Create MDTM tasks
│   ├── opinion.md                 # /rf:opinion - Anti-sycophancy analysis
│   └── opinion_v2_deterministic.md # /rf:opinion_v2 - Deterministic analysis
│
└── hooks/                         # Session hooks
    ├── ibtask_prompt.py           # Task execution hook
    └── load-context2.py           # Auto-load framework rules on session start
```

---

## .dev/ - Development & Task Management

```
.dev/
├── taskplanning/                  # Development planning & milestones
│   ├── backlog/                   # Planning documents
└── tasks/                         # MDTM Task Files
    ├── example_tasks/             # Example task files
    │   └── Example-TASK-SAMPLE-DEMO-NEW.md
    └── taskbuildernotes/          # Taskbuilder session notes
```

---

## .claude/ - Framework Core

```
.claude/
├── changelogs/                    # Release changelogs
│   ├── README.md                  # Changelog system documentation
│   ├── 2025-10-08_v5.1.0_ENHANCEMENTS.md
│   ├── 2025-10-11_v5.1.1_FIXES.md
│   ├── 2025-10-14_v5.1.2_FIXES.md
│   ├── 2025-10-15_v5.1.3_CHANGES.md
│   ├── 2025-10-19_v5.1.4_DOCUMENTATION_CONSOLIDATION.md
│   ├── 2025-10-22_v5.2.0_UID_CONTENT_SYNC_AND_SECURITY.md
│   └── changelog_workspace/       # Merge analysis & gap docs (5 files)
│
├── docs/                          # User Documentation
│   ├── DIRECTORY_STRUCTURE.md     # Directory structure reference (duplicated to ~/.claude/rules/core/)
│   └── guides/                    # User guides (6 files)
│       ├── anti_sycophancy_guide.md
│       ├── qa_validation_guide.md
│       ├── RIGORFLOW_BATCH_STATE_FLOW_GUIDE.md
│       ├── rigorflow_framework_changes_guide.md
│       ├── rigorflow_workflow_deep_dive_guide.md
│       └── tool_performance_benchmarks_guide.md
│
├── rules/                         # Framework Rules & Standards
│   ├── core/                      # Core rules (9 files)
│   │   ├── anti_hallucination_task_completion_rules.md
│   │   ├── anti_sycophancy.md
│   │   ├── changelog_maintenance.md
│   │   ├── DIRECTORY_STRUCTURE.md (duplicated from .claude/docs/)
│   │   ├── file_conventions.md
│   │   ├── ib_agent_core.md
│   │   ├── quality_gates.md
│   │   └── tool_selection.md
│   │
│   ├── contextual/                # Contextual rules
│   │   └── context_embedding.md
│   │
│   └── prompts/                   # Agent prompts (9 files)
│       ├── agent_library.md
│       ├── automated_qa_workflow_worker_prompt.md
│       ├── automated_qa_workflow_qa_prompt.md
│       ├── doc_code_analyst_worker_prompt.md
│       ├── doc_code_analyst_qa_prompt.md
│       ├── documentation_expert_worker_prompt.md
│       ├── documentation_expert_qa_prompt.md
│       ├── recruiting_expert_worker_prompt.md
│       └── recruiting_expert_qa_prompt.md
│
├── scripts/                       # Framework Scripts
│   ├── automated_qa_workflow.sh                    # Main orchestrator
│   ├── automated_qa_workflow_backup_*.sh           # Backups (4 files)
│   ├── compute_uid_index.py                        # UID computation
│   ├── compute_uid_index_backup_20251022_1220p.py
│   ├── input_validation.sh                         # Input validation
│   ├── parse_checklist.py                          # Checklist parser
│   ├── rollover_context_functions.sh               # Session rollover
│   ├── session_message_counter.sh                  # Message counting
│   └── UID_fail_item_match_fallback.py            # UID fallback
│
├── templates/                     # Task & Document Templates
│   ├── 01_mdtm_template_generic_task.md
│   ├── changelog_template.md
│   └── qa_validation_checklist_template.md
│
└── tests/                         # Test Suites
    ├── baseline/                  # Baseline tests
    │   ├── enhanced_v1/           # Enhanced template v1 tests (5 files)
    │   ├── enhanced_v2/           # Enhanced template v2 tests (6 files)
    │   ├── BASELINE_METRICS.md
    │   ├── COMPATIBILITY_REPORT.md
    │   ├── MILESTONE_0_COMPLETION_REPORT.md
    │   ├── run_baseline_tests.sh
    │   ├── TEST_ENHANCED_SAMPLE.md
    │   └── TEST_TASK_[1-5].md     # 5 baseline test tasks
    │
    ├── security_audit.sh
    └── test_task_template_enhancement_performance.sh
```

---

## File Count Summary

| Directory | Files | Purpose |
|-----------|-------|---------|
| **Root** | 4 | Project documentation & releases |
| **.claude/** | 6 | Claude Code configuration & commands |
| **.dev/taskplanning/** | - | Development planning (not detailed here) |
| **.dev/tasks/** | 5 | Active & example MDTM tasks |
| **.claude/changelogs/** | 11 | Release changelogs & merge analysis |
| **.claude/docs/guides/** | 6 | User guides |
| **~/.claude/rules/core/** | 9 | Core framework rules |
| **~/.claude/rules/contextual/** | 1 | Contextual rules |
| **~/.claude/rules/prompts/** | 9 | Agent prompts |
| **.claude/scripts/** | 13 | Framework orchestration & utilities |
| **.claude/templates/** | 3 | Task & document templates |
| **.claude/tests/** | 20+ | Test suites & reports |

---

## Navigation Guide

### For Users Starting with Rigorflow
**Start here:** `README.md` (root)
- Quick start: Run `/rf:task` or `/rf:taskbuilder`
- User guides: `.claude/docs/guides/`

### For Framework Developers
**Start here:** `.claude/docs/guides/`
- Workflow deep dive: `rigorflow_workflow_deep_dive_guide.md`
- Framework changes: `rigorflow_framework_changes_guide.md`
- Batch state flow: `rigorflow_batch_state_flow_guide.md`

### For Rule & Prompt Customization
**Start here:** `~/.claude/rules/`
- Core rules: `core/` (9 files)
- Agent prompts: `prompts/` (9 files)
- Agent library: `prompts/agent_library.md`

### For Changelog Maintenance
**Start here:** `.claude/changelogs/README.md`
- Master changelog: Root `CHANGELOG.md`
- Detailed releases: `.claude/changelogs/YYYY-MM-DD_vX.Y.Z_*.md`
- Rules: `~/.claude/rules/core/changelog_maintenance.md`

---

## Key Principles

### Organization
1. **Framework core** lives in `.claude/`
2. **Development work** lives in `.dev/`
3. **Configuration** lives in `.claude/`
4. **User-facing docs** at root and `.claude/docs/`

### Exclusions
- **Workflow artifacts** not documented (`.claude/.state`, `.dev/tasks/*/`)
- **Internal dev directories** not documented (`.claude/.dev`)
- **Git artifacts** not documented (`.git/`)

### Versioning
- Semantic versioning: `MAJOR.MINOR.PATCH`
- Planning organized by version: `.dev/taskplanning/vX.Y/`
- Changelogs follow Keep a Changelog format

---

**Structure Version:** 2.0
**Last Full Update:** 2025-10-29
