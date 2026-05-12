# Workflow: Fix Broken Template Paths

**Generated**: 2026-04-03
**Source**: `docs/generated/broken-path-index.md`
**Branch**: `refactor/prd-skill-decompose`

---

## Path Mapping

| Wrong Path | Correct Path |
|-----------|-------------|
| `docs/docs-product/templates/prd_template.md` | `src/superclaude/examples/prd_template.md` |
| `docs/docs-product/templates/tdd_template.md` | `src/superclaude/examples/tdd_template.md` |
| `.gfdoc/templates/02_mdtm_template_complex_task.md` | `.claude/templates/workflow/02_mdtm_template_complex_task.md` |
| `.gfdoc/templates/01_mdtm_template_generic_task.md` | `.claude/templates/workflow/01_mdtm_template_generic_task.md` |

---

## Parallelization Strategy

Each task edits exactly ONE file. Files have zero overlap, so all tasks within a wave can run in parallel.

### Wave 1 — Source files (src/superclaude/) — ALL PARALLEL

These 12 tasks touch independent files. No dependencies between them.

### Wave 2 — Non-src files — ALL PARALLEL

These 4 tasks touch files outside `src/` that have no src/ mirror.

### Wave 3 — Sync + Verify (SEQUENTIAL, depends on Wave 1 + Wave 2)

Single task: run `make sync-dev` then `make verify-sync`.

---

## Tasks

### Wave 1: Source Files (all parallel — no overlapping files)

#### Task 1: Fix `src/superclaude/skills/prd/SKILL.md`
- **Replacements**: 12 (10× `docs/docs-product/templates/prd_template.md` → `src/superclaude/examples/prd_template.md`, 2× `.gfdoc/templates/` → `.claude/templates/workflow/`)
- **Lines**: 12, 127, 368, 464, 713, 848, 874, 925, 993, 1135, 520, 521
- **Method**: `replace_all` for each wrong string

#### Task 2: Fix `src/superclaude/skills/prd/refs/agent-prompts.md`
- **Replacements**: 4× `docs/docs-product/templates/prd_template.md` → `src/superclaude/examples/prd_template.md`
- **Lines**: 150, 285, 311, 362

#### Task 3: Fix `src/superclaude/skills/prd/refs/synthesis-mapping.md`
- **Replacements**: 1× `docs/docs-product/templates/prd_template.md` → `src/superclaude/examples/prd_template.md`
- **Lines**: 12

#### Task 4: Fix `src/superclaude/skills/prd/refs/validation-checklists.md`
- **Replacements**: 1× `docs/docs-product/templates/prd_template.md` → `src/superclaude/examples/prd_template.md`
- **Lines**: 15

#### Task 5: Fix `src/superclaude/skills/tdd/SKILL.md`
- **Replacements**: 2× `docs/docs-product/templates/tdd_template.md` → `src/superclaude/examples/tdd_template.md`
- **Lines**: 12, 125

#### Task 6: Fix `src/superclaude/skills/tdd/refs/build-request-template.md`
- **Replacements**: 4 (2× `docs/docs-product/templates/tdd_template.md` → `src/superclaude/examples/tdd_template.md`, 2× `.gfdoc/templates/` → `.claude/templates/workflow/`)
- **Lines**: 80, 114, 133, 134

#### Task 7: Fix `src/superclaude/skills/tdd/refs/agent-prompts.md`
- **Replacements**: 4× `docs/docs-product/templates/tdd_template.md` → `src/superclaude/examples/tdd_template.md`
- **Lines**: 150, 286, 312, 361

#### Task 8: Fix `src/superclaude/skills/tdd/refs/synthesis-mapping.md`
- **Replacements**: 1× `docs/docs-product/templates/tdd_template.md` → `src/superclaude/examples/tdd_template.md`
- **Lines**: 5

#### Task 9: Fix `src/superclaude/skills/tdd/refs/validation-checklists.md`
- **Replacements**: 1× `docs/docs-product/templates/tdd_template.md` → `src/superclaude/examples/tdd_template.md`
- **Lines**: 9

#### Task 10: Fix `src/superclaude/skills/tdd/refs/operational-guidance.md`
- **Replacements**: 1× `docs/docs-product/templates/tdd_template.md` → `src/superclaude/examples/tdd_template.md`
- **Lines**: 82

#### Task 11: Fix `src/superclaude/examples/prd_template.md`
- **Replacements**: 1× `docs/docs-product/templates/prd_template.md` → `src/superclaude/examples/prd_template.md`
- **Lines**: 1318

#### Task 12: Fix `docs/guides/prd-skill-release-guide.md`
- **Replacements**: 1× `docs/docs-product/templates/prd_template.md` → `src/superclaude/examples/prd_template.md`
- **Lines**: 73

### Wave 2: Non-src files without mirrors (all parallel)

#### Task 13: Fix `docs/guides/tdd-skill-release-guide.md`
- **Replacements**: 2× `docs/docs-product/templates/tdd_template.md` → `src/superclaude/examples/tdd_template.md`
- **Lines**: 81, 687

#### Task 14: Fix `.claude/skills/tech-research/SKILL.md` (NO src/ mirror — edit directly)
- **Replacements**: 2× `.gfdoc/templates/` → `.claude/templates/workflow/`
- **Lines**: 438, 439
- **NOTE**: This file has no `src/superclaude/skills/tech-research/` source copy. Edit in-place.

### Wave 3: Sync & Verify (sequential, depends on Wave 1 + 2)

#### Task 15: Run `make sync-dev` and `make verify-sync`
- **Action**: Propagate all `src/superclaude/` changes to `.claude/` dev copies
- **Verification**: `make verify-sync` must pass with zero diffs
- **Post-check**: `grep -r "docs/docs-product/templates" src/superclaude/skills/ .claude/skills/` must return 0 results
- **Post-check**: `grep -r "\.gfdoc/templates" src/superclaude/skills/ .claude/skills/` must return 0 results

---

## Validation Criteria

After all waves complete:
1. `grep -r "docs/docs-product/templates" src/superclaude/skills/ .claude/skills/ src/superclaude/examples/ docs/guides/` → 0 results
2. `grep -r "\.gfdoc/templates" src/superclaude/skills/ .claude/skills/` → 0 results
3. `make verify-sync` → passes
4. All template paths in skills point to files that exist on disk
