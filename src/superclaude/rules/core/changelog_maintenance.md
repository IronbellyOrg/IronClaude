---
title: Changelog Maintenance Rules
description: "Required process for maintaining framework changelogs following Keep a Changelog and Semantic Versioning standards. Defines mandatory changelog update process, decision matrix for detailed release files, semantic versioning rules, and GitHub release integration."
id: "changelog-maintenance-rules"
sidebar_position: 6
created_date: "2025-10-11"
last_updated: "2025-10-11"
version: 1.0.0
draft: false
content_status: Published
tags:
- changelog
- documentation
- rules
- versioning
- "semantic-versioning"
- "release-process"
content_type: Rule
target_audience:
- Developer
- SystemArchitect
- AI
- Machine
owner: "framework-team"
autogen: false
autogen_method: ""
autogen_source: []
autogen_version: ""
ai_model: ""
model_settings: ""
related_links:
- text: Master CHANGELOG.md
  link: CHANGELOG.md
- text: Changelog System README
  link: .claude/changelogs/README.md
- text: Changelog Template
  link: .claude/templates/workflow/changelog_template.md
- text: File Conventions
  link: ~/.claude/rules/core/file_conventions.md
related_task_id:
- "TASK-CHANGELOG-20251011-155000-SystemSetup"
review_info:
  last_reviewed_by: "framework-team"
  last_review_date: "2025-10-11"
  next_review_date: "2026-04-11"
---

# Changelog Maintenance Rules

## Purpose

All framework changes MUST be documented following Keep a Changelog format and Semantic Versioning standards. This ensures transparency, traceability, and proper version management.

---

## Mandatory Process

### During Development

**ALWAYS** add changes to "Unreleased" section in `CHANGELOG.md`:

```markdown
## [Unreleased]

### Added
- New feature description

### Fixed
- Bug fix description
```

**Categories**: Added, Changed, Deprecated, Removed, Fixed, Security

---

### Before Release

#### Step 1: Determine if Detailed File Needed

Use this decision matrix:

| Size | Criteria | Create Detailed File? |
|------|----------|----------------------|
| **Tiny** | 1-2 trivial changes | ❌ No - CHANGELOG.md only |
| **Small** | 3-10 changes, single area, no breaking changes | ❌ No - CHANGELOG.md with bullets |
| **Medium** | 10-30 changes, multiple areas, OR migration needed | ✅ Yes |
| **Large** | 30+ changes, breaking changes, major features | ✅ Yes |

**ALWAYS create detailed file if:**
- New major/minor version (X.0.0 or X.Y.0)
- Breaking changes or deprecations
- New features requiring documentation
- Architectural changes
- Migration guides needed
- Performance impact > 10%
- 10+ files changed

**DON'T create detailed file if:**
- Patch fixes (X.Y.Z) with <10 changes, no breaking changes
- Single-file documentation updates, typo fixes
- Internal refactoring with no user impact, test-only changes

#### Step 2: Create Detailed File (if needed)

1. Copy template: `.claude/templates/workflow/changelog_template.md`
2. Name: `YYYY-MM-DD_vX.Y.Z_SHORT_DESCRIPTION.md`
3. Save to: `.claude/changelogs/`
4. Fill ALL required sections (see template)

#### Step 3: Update CHANGELOG.md

1. Move "Unreleased" items to new `[X.Y.Z] - YYYY-MM-DD` section
2. Add link to detailed file (if created):
   ```markdown
   **Detailed Release Notes**: [.claude/changelogs/YYYY-MM-DD_vX.Y.Z_DESCRIPTION.md]
   ```
3. Update comparison links at bottom

---

### After Release

#### Step 4: Git Tagging

```bash
git tag -a vX.Y.Z -m "Release vX.Y.Z - Brief Description"
git push origin vX.Y.Z
```

#### Step 5: GitHub Release (if using GitHub)

**Option A - CLI** (recommended):
```bash
gh release create vX.Y.Z \
  --title "vX.Y.Z - Brief Description" \
  --notes-file .claude/changelogs/YYYY-MM-DD_vX.Y.Z_DESCRIPTION.md
```

**Option B - Web UI**: See `.claude/changelogs/README.md` section 4

#### Step 6: Start New Unreleased Section

Add to top of `CHANGELOG.md`:
```markdown
## [Unreleased]

### Added
- (items will be added as development continues)
```

---

## Semantic Versioning

**MAJOR.MINOR.PATCH**

- **MAJOR (X.0.0)**: Breaking changes, incompatible API changes
- **MINOR (X.Y.0)**: New features, backward-compatible
- **PATCH (X.Y.Z)**: Bug fixes, documentation, backward-compatible

---

## Files and Locations

- **Master Changelog**: `CHANGELOG.md` (repository root)
- **Detailed Files**: `.claude/changelogs/YYYY-MM-DD_vX.Y.Z_DESCRIPTION.md`
- **Template**: `.claude/templates/workflow/changelog_template.md`
- **Documentation**: `.claude/changelogs/README.md` (human reference)

---

## Enforcement

- ✅ **MUST** update CHANGELOG.md for every significant change
- ✅ **MUST** follow decision matrix for detailed files
- ✅ **MUST** use semantic versioning correctly
- ✅ **MUST** create git tags for all releases
- ❌ **NEVER** skip changelog updates
- ❌ **NEVER** use vague descriptions ("various fixes")
- ❌ **NEVER** forget migration notes for breaking changes

---

**Related Documentation**: See `.claude/changelogs/README.md` for detailed examples, best practices, and troubleshooting.
