# D-0022: Retained Content Validation (FR-TDD-R.1b through FR-TDD-R.1e)

**Task:** T04.06
**Date:** 2026-04-03
**File:** `src/superclaude/skills/tdd/SKILL.md` (438 lines)
**Overall Result:** PARTIAL PASS (4/5 categories present, 1 missing)

---

## Per-Category Validation

### FR-TDD-R.1b: Frontmatter and Extended Metadata
**Result:** PASS

| Element | Location | Evidence |
|---------|----------|----------|
| YAML frontmatter | Lines 1-4 | `---` delimiters with `name: tdd` and `description: "..."` |
| Extended metadata | Lines 1-4 | `description` field contains full trigger phrase catalog (287 chars) |

### FR-TDD-R.1c: Purpose, Input, and Tier Sections
**Result:** PASS

| Section | Location | Evidence |
|---------|----------|----------|
| Purpose | Lines 6-30 | `# TDD Creator` heading + "Why This Process Works" subsection |
| Input | Lines 33-76 | `## Input` with 4 information pieces, effective prompt examples, incomplete prompt template |
| Tier Selection | Lines 80-95 | `## Tier Selection` with Lightweight/Standard/Heavyweight table and selection rules |

### FR-TDD-R.1d: Stage A Protocol and Stage B Delegation Protocol
**Result:** PASS

| Section | Location | Evidence |
|---------|----------|----------|
| Execution Overview | Lines 133-160 | `## Execution Overview` with Stage A (8 steps) and Stage B (2 steps) summary |
| Stage A | Lines 164-389 | `## Stage A: Scope Discovery & Task File Creation` with subsections A.1-A.8 |
| Stage B | Lines 396-414 | `## Stage B: Task File Execution` with delegation protocol and task file requirements |

### FR-TDD-R.1e (part 1): Will Do / Will Not Do Boundaries
**Result:** FAIL

The SKILL.md does **not** contain an explicit "Will Do / Will Not Do" or "Boundaries" section. This pattern exists in other skills (sc-roadmap-protocol, sc-adversarial-protocol, sc-cli-portify-protocol, sc-cleanup-audit-protocol, etc.) but was never present in the original TDD SKILL.md and was not added during the refactor.

**Grep evidence:**
```
$ grep -i "will do\|will not do\|## Boundaries\|### Will" src/superclaude/skills/tdd/SKILL.md
(no matches)
```

**Remediation required:** Add a "Boundaries" section with "Will Do" and "Will Not Do" subsections to SKILL.md, following the pattern established by other skills.

### FR-TDD-R.1e (part 2): Explicit Refs Loading Declarations
**Result:** PASS

| Declaration | Location | Evidence |
|-------------|----------|----------|
| Orchestrator load (A.7) | Lines 345-348 | `Read refs/build-request-template.md` directive with FR-TDD-R.6a citation |
| Builder load deps (A.7) | Lines 355-360 | 4 `Read refs/*.md` directives with FR-TDD-R.6b citation |
| Load-point markers | Lines 353, 366, 368, 370, 372 | 5 `> **Loaded at runtime from**` blockquote markers |
| Phase Loading Contract | Lines 418-429 | Full phase-to-refs mapping table (FR-TDD-R.6c) |
| Contract validation | Lines 431-435 | Set intersection and runtime containment rules (FR-TDD-R.6d) |

**Refs files existence verified:**
- `refs/build-request-template.md` -- EXISTS
- `refs/agent-prompts.md` -- EXISTS
- `refs/synthesis-mapping.md` -- EXISTS
- `refs/validation-checklists.md` -- EXISTS
- `refs/operational-guidance.md` -- EXISTS

---

## Summary

| Requirement | Category | Result |
|-------------|----------|--------|
| FR-TDD-R.1b | Frontmatter + metadata | PASS |
| FR-TDD-R.1c | Purpose / Input / Tier | PASS |
| FR-TDD-R.1d | Stage A + Stage B protocols | PASS |
| FR-TDD-R.1e (boundaries) | Will Do / Will Not Do | **FAIL** |
| FR-TDD-R.1e (refs) | Refs loading declarations | PASS |

## Remediation

**One defect found:** Missing "Will Do / Will Not Do" boundaries section.

**Suggested fix:** Add after the Phase Loading Contract section (after line 435) a `## Boundaries` section with `### Will Do` and `### Will Not Do` subsections following the established pattern from other skills. Example content:

```markdown
## Boundaries

### Will Do
- Create comprehensive TDDs by researching actual codebase
- Spawn parallel subagents for deep investigation
- Produce template-aligned technical design documents
- Translate PRD requirements into engineering specifications
- Resume from existing task files and research

### Will Not Do
- Modify source code (read-only investigation)
- Fabricate design specifications without codebase evidence
- Generate code snippets unless documenting existing patterns
- Skip quality gates (analyst verification, QA checks)
- Execute the design (produces plans, not implementations)
```

This would add ~15 lines, keeping the file well under the 500-line budget (438 + 15 = ~453).
