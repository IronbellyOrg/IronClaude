# D-0002: SKILL.md Baseline SHA Record

## Task: T01.02 -- Freeze SKILL.md baseline SHA

**Target file:** `.claude/skills/prd/SKILL.md`
**Date:** 2026-04-03
**Branch:** `feat/tdd-spec-merge`

## SHA Records

| Version | SHA | Source |
|---------|-----|--------|
| Working tree (baseline) | `db4352ff0dd9c0869eab5f6c365c4af900c1fdfa` | `git hash-object .claude/skills/prd/SKILL.md` |
| Last committed (HEAD) | `9e32d267c83e07a1786e2965b99a0048a8f8e414` | `git rev-parse HEAD:.claude/skills/prd/SKILL.md` |

## Pending Changes Status

**Working tree has unstaged modifications** relative to HEAD commit.

**Diff summary:** 1 file changed, 21 insertions(+), 42 deletions(-)

**Nature of changes:**
1. Template path updates: `.claude/templates/documents/prd_template.md` changed to `docs/docs-product/templates/prd_template.md` (3 occurrences)
2. Removed `QA_GATE_REQUIREMENTS`, `VALIDATION_REQUIREMENTS`, and `TESTING_REQUIREMENTS` blocks from BUILD_REQUEST section (~13 lines)
3. Removed `**ADVERSARIAL STANCE:**` inline directives from Phase 3, Phase 5, and Phase 6 QA spawn instructions (~3 occurrences)

## Baseline Decision

**Frozen baseline SHA: `db4352ff0dd9c0869eab5f6c365c4af900c1fdfa`** (working tree)

Rationale: The fidelity index (`fidelity-index.md`) was built against the 1,373-line working-tree version. The working-tree file is 1,373 lines, matching the fidelity index's total line count. All Phase 2 extraction line ranges reference this version. Implementation MUST proceed against this SHA.

## Verification

- SHA is valid 40-character hex string: YES
- Line count: 1,373 (matches fidelity index expectation)
- Baseline SHA frozen for drift detection: any future `git hash-object .claude/skills/prd/SKILL.md` that differs from `db4352ff0dd9c0869eab5f6c365c4af900c1fdfa` indicates the file was modified after baseline freeze

## Risk Mitigation (Risk #7 -- Spec Freshness)

Before starting any Phase 2 extraction task, verify:
```bash
[ "$(git hash-object .claude/skills/prd/SKILL.md)" = "db4352ff0dd9c0869eab5f6c365c4af900c1fdfa" ] && echo "MATCH" || echo "DRIFT DETECTED"
```
