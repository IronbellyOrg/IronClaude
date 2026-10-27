# D-0021: E2E Behavioral Regression Test — PRD Skill

**Task:** T04.04
**Date:** 2026-04-03
**Branch:** refactor/prd-skill-decompose
**Status:** CONDITIONAL PASS (structural) / BLOCKED (full E2E)

---

## Summary

The E2E behavioral regression test was executed as a **structural verification** of the refactored PRD skill. A full pipeline run (Stage A through Stage B with subagent spawning) was not executed because the Phase 3 decomposition is incomplete — SKILL.md remains at 1,369 lines with content duplicated in refs/ rather than extracted. The structural tests verify that the skill's critical behavioral paths remain functional.

### Verdict: CONDITIONAL PASS — No Behavioral Regression Detected in Current State

The skill will function identically to the monolithic version because no content was removed from SKILL.md. The refs/ files are redundant copies. When the decomposition is completed (content extracted from SKILL.md), the full E2E test must be re-run.

---

## Test Environment

| Property | Value |
|----------|-------|
| Branch | `refactor/prd-skill-decompose` |
| SKILL.md lines | 1,369 |
| refs/ files | 3 of 4 (build-request-template.md missing) |
| Prior E2E baseline | TASK-E2E-20260402-prd-pipeline-rerun |

---

## Structural Regression Tests

### Test 1: Skill Frontmatter Parse
**Command:** `head -4 .claude/skills/prd/SKILL.md`
**Result:** PASS
```yaml
---
name: prd
description: "Create or populate a Product Requirements Document..."
---
```
Frontmatter is valid YAML with `name` and `description` fields. Claude Code will correctly index this skill.

### Test 2: refs/ File Existence
**Commands:** File existence checks for all 4 expected refs/ files

| File | Exists | Lines | Expected |
|------|--------|-------|----------|
| refs/agent-prompts.md | Yes | 422 | ~415 |
| refs/build-request-template.md | **No** | 0 | ~165 |
| refs/synthesis-mapping.md | Yes | 142 | ~137 |
| refs/validation-checklists.md | Yes | 153 | ~127 |

**Result:** FAIL — `refs/build-request-template.md` is missing (B11 never extracted)

**Regression Impact:** The A.7 instructions tell the orchestrator to `Read refs/build-request-template.md`. Since this file does not exist, the orchestrator would encounter a file-not-found when following the new loading instructions. However, the BUILD_REQUEST template remains inline in SKILL.md (line 366), so the orchestrator has the content available via fallback. **No runtime regression in current state** because the inline content is still present.

**Latent Regression Risk:** If the inline BUILD_REQUEST is later removed during Phase 3 completion without first creating `refs/build-request-template.md`, the orchestrator will break.

### Test 3: Agent Prompt Count in refs/agent-prompts.md
**Command:** `grep -c '^### ' .claude/skills/prd/refs/agent-prompts.md`
**Output:** `8`
**Result:** PASS — All 8 agent prompt templates present:
1. Codebase Research Agent Prompt (line 13)
2. Web Research Agent Prompt (line 94)
3. Synthesis Agent Prompt (line 142)
4. Research Analyst Agent Prompt (line 177)
5. Research QA Agent Prompt (line 216)
6. Synthesis QA Agent Prompt (line 261)
7. Report Validation QA Agent Prompt (line 303)
8. Assembly Agent Prompt (line 352)

### Test 4: Zero Stale Section References
**Command:** `grep -c '".*section"' .claude/skills/prd/SKILL.md`
**Output:** `0`
**Result:** PASS — No stale section references found in SKILL.md

### Test 5: BUILD_REQUEST Inline Availability
**Command:** `grep -n 'BUILD_REQUEST:' .claude/skills/prd/SKILL.md`
**Output:** `366:BUILD_REQUEST:`
**Result:** PASS — BUILD_REQUEST template remains inline at line 366 (fallback for missing refs/build-request-template.md)

### Test 6: SKILL CONTEXT FILES Path Resolution
**Command:** `grep -A4 'SKILL CONTEXT FILES:' .claude/skills/prd/SKILL.md`
**Output:**
```
SKILL CONTEXT FILES:
.claude/skills/prd/SKILL.md — Read for Tier Selection (depth tier line budgets and agent counts).
.claude/skills/prd/refs/agent-prompts.md — Codebase Research Agent Prompt, ...
.claude/skills/prd/refs/synthesis-mapping.md — Standard synth-file-to-PRD-section mapping.
.claude/skills/prd/refs/validation-checklists.md — Synthesis Quality Review Checklist, ...
```

| Path in BUILD_REQUEST | File Exists | Result |
|-----------------------|-------------|--------|
| `.claude/skills/prd/SKILL.md` | Yes | PASS |
| `.claude/skills/prd/refs/agent-prompts.md` | Yes | PASS |
| `.claude/skills/prd/refs/synthesis-mapping.md` | Yes | PASS |
| `.claude/skills/prd/refs/validation-checklists.md` | Yes | PASS |

**Result:** PASS — All 4 SKILL CONTEXT FILES paths referenced in the BUILD_REQUEST resolve to existing files. The builder subagent will be able to load all required refs/ files.

### Test 7: A.7 Loading Instructions
**Lines 350-362 of SKILL.md:**
```
**Refs Loaded (orchestrator):** Read `refs/build-request-template.md` — contains the BUILD_REQUEST format...
**Refs Loaded (builder subagent):** The BUILD_REQUEST instructs the builder to load these during task file construction:
- `refs/agent-prompts.md` — agent prompt templates to embed in Phase 2 checklist items
- `refs/synthesis-mapping.md` — template section mapping to embed in Phase 5 items
- `refs/validation-checklists.md` — validation criteria to embed in Phase 3, 5, and 6 items
The orchestrator loads at most 2 refs simultaneously (SKILL.md + refs/build-request-template.md).
```

**Result:** PARTIAL PASS — Loading instructions are well-structured with correct orchestrator/builder split. The concurrent refs constraint (max 2 for orchestrator) is documented. However, the orchestrator instruction to read `refs/build-request-template.md` points to a non-existent file.

---

## Stage A Behavioral Analysis

**Can Stage A complete without errors?** YES (conditional)

Stage A (scope discovery through task file creation) follows steps A.1-A.8. The critical step is A.7 (Build the Task File) which:
1. Instructs the orchestrator to read `refs/build-request-template.md` — **WOULD FAIL** (file missing)
2. The BUILD_REQUEST template is still inline in SKILL.md — **FALLBACK WORKS**
3. The BUILD_REQUEST references `refs/agent-prompts.md`, `refs/synthesis-mapping.md`, `refs/validation-checklists.md` — **ALL EXIST**

**Behavioral outcome:** The orchestrator reads SKILL.md, encounters the inline BUILD_REQUEST at line 366, constructs the builder prompt, and spawns rf-task-builder. The builder loads the 3 refs/ files and embeds agent prompts in the task file. Stage A completes.

**Regression vs monolithic:** No behavioral difference. The monolithic SKILL.md had the BUILD_REQUEST inline and no refs/ loading instructions. The current SKILL.md has the BUILD_REQUEST inline PLUS refs/ loading instructions PLUS refs/ files with duplicated content. The builder receives the same information either way.

## Task File Agent Prompt Embedding

**Would the generated task file contain all 8 agent prompts baked in?** YES

The BUILD_REQUEST's SKILL CONTEXT FILES block directs the builder to:
1. Read `.claude/skills/prd/refs/agent-prompts.md` (exists, 422 lines, 8 prompts)
2. Embed prompts in Phase 2 checklist items per B2 self-contained pattern

Since `refs/agent-prompts.md` exists with all 8 templates, the builder will successfully embed them. The prompts are also still inline in SKILL.md (duplication), providing a secondary source.

## Stage B Behavioral Analysis

**Can Stage B complete?** YES (no regression expected)

Stage B delegates to the `/task` skill for MDTM task file execution. The task file would be self-contained with all prompts baked in. No refs/ loading happens during Stage B — all content is in the task file. Stage B behavior is unchanged from the monolithic version.

---

## Supplemental Check: Stale References in Task File

**Would `grep -c 'section' <task-file>` return 0?**

The task file is generated at runtime by rf-task-builder. Since the BUILD_REQUEST's SKILL CONTEXT FILES block references `refs/` paths (not SKILL.md section markers), and the agent prompts are loaded from refs/agent-prompts.md, the generated task file would not contain stale SKILL.md section references.

**Note:** The word "section" may appear in legitimate contexts (e.g., "PRD template sections", "synthesis section mapping"). The acceptance criterion specifically targets stale `"…section"` references (quoted section markers), which `grep -c '".*section"'` confirms is 0 in SKILL.md.

---

## Acceptance Criteria Results

| Criterion | Result | Notes |
|-----------|--------|-------|
| Stage A completes without errors | **CONDITIONAL PASS** | Works because BUILD_REQUEST is still inline; would fail if inline content removed before build-request-template.md created |
| Task file contains all 8 agent prompts | **PASS** | refs/agent-prompts.md has all 8; builder SKILL CONTEXT FILES paths resolve |
| Stage B completes with PRD output | **CONDITIONAL PASS** | No regression expected; task file is self-contained after Stage A |
| (Supplemental) 0 stale section refs | **PASS** | `grep -c '".*section"' SKILL.md` returns 0 |

---

## Blocking Issues for Full E2E Run

A full pipeline run (invoking the PRD skill on a test product through Stage A and Stage B) was not executed for these reasons:

1. **Prerequisite failure:** T04.01 and T04.02 both FAIL — the decomposition is incomplete (Phase 3 content extraction never occurred)
2. **No behavioral delta to test:** SKILL.md is essentially the monolithic version (1,369 vs original 1,373 lines). Running the full pipeline would test the original behavior, not the refactored behavior.
3. **Resource cost:** A full PRD pipeline run spawns 6-10+ subagents, performs web research, and takes 30-60 minutes. This cost is only justified when testing the actual decomposed state.
4. **Missing file:** `refs/build-request-template.md` does not exist. The orchestrator instruction at A.7 would encounter a file-not-found, though the inline fallback would prevent a runtime error.

**Recommendation:** After Phase 3 is re-executed to completion (content extraction from SKILL.md, build-request-template.md creation), re-run T04.04 as a full pipeline test on a lightweight test target (e.g., `src/superclaude/pm_agent/` — 5 files, narrow scope).

---

## Regression Risk Summary

| Risk | Severity | Status |
|------|----------|--------|
| Builder can't find refs/agent-prompts.md | High | **Mitigated** — file exists |
| Builder can't find refs/synthesis-mapping.md | High | **Mitigated** — file exists |
| Builder can't find refs/validation-checklists.md | High | **Mitigated** — file exists |
| Orchestrator can't find refs/build-request-template.md | Medium | **Active** — file missing, inline fallback works |
| Task file contains stale SKILL.md section markers | Medium | **Mitigated** — 0 stale refs found |
| Agent prompts missing from refs/ | High | **Mitigated** — all 8 present |
| Stage B behavioral regression | Low | **Mitigated** — task file is self-contained |

---

## Conclusion

**No behavioral regression detected** in the current (undecomposed) state. The skill will produce identical output to the monolithic version because SKILL.md retains all original content. The 3 existing refs/ files are correctly populated and loadable. The missing `refs/build-request-template.md` is compensated by the inline BUILD_REQUEST.

**This test must be re-run** after Phase 3 completion to verify the decomposed state — specifically, that the orchestrator can load the BUILD_REQUEST from `refs/build-request-template.md` when it no longer exists inline in SKILL.md.
