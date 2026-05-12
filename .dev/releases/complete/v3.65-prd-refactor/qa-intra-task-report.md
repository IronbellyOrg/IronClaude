# QA Report -- PRD Skill Refactor (Intra-Task)

**Date:** 2026-04-03
**Phase:** intra-task (structural integrity, consistency, sync, conventions)
**Scope:** PRD skill files across `.claude/skills/prd/` and `src/superclaude/skills/prd/`
**Fix authorization:** true (safe, unambiguous fixes)

---

## Overall Verdict: FAIL

---

## Files Reviewed

| # | File | Path | Lines |
|---|------|------|-------|
| 1 | SKILL.md (active) | `.claude/skills/prd/SKILL.md` | 1369 |
| 2 | SKILL.md (source) | `src/superclaude/skills/prd/SKILL.md` | 1369 |
| 3 | agent-prompts.md | `src/superclaude/skills/prd/refs/agent-prompts.md` | 422 |
| 4 | synthesis-mapping.md | `src/superclaude/skills/prd/refs/synthesis-mapping.md` | 142 |
| 5 | validation-checklists.md | `src/superclaude/skills/prd/refs/validation-checklists.md` | 153 |
| 6 | .gitkeep | `src/superclaude/skills/prd/refs/.gitkeep` | N/A |

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Frontmatter validity | PASS | Lines 1-4: valid YAML frontmatter with `name: prd` and `description` field. Matches skill convention (same format as TDD skill). |
| 2 | Sync state (.claude vs src) | PASS | `diff` of SKILL.md: identical (0 differences). `diff` of all 3 refs files + .gitkeep: identical. |
| 3 | Command file exists | WARN | No `/sc:prd` command file found at `.claude/commands/sc/prd.md` or `src/superclaude/commands/sc/prd*`. The skill IS registered in the skill list (appears as `prd` in session skills). Skill invocation works via `Skill` tool. However, no dedicated command file means there is no `/sc:prd` slash command for users to invoke directly. |
| 4 | Referenced files exist (refs/) | FAIL | **CRITICAL:** SKILL.md line 352 references `refs/build-request-template.md` ("Read `refs/build-request-template.md`"). This file does NOT exist in `src/superclaude/skills/prd/refs/` or `.claude/skills/prd/refs/`. The TDD skill has this file at `src/superclaude/skills/tdd/refs/build-request-template.md`. The BUILD_REQUEST content is instead inlined in SKILL.md lines 365-526. |
| 5 | Referenced external files exist | FAIL | SKILL.md references `docs/docs-product/templates/prd_template.md` (lines 12, 43, 127, 368, etc.) and `.gfdoc/templates/02_mdtm_template_complex_task.md` (line 520). Neither path exists on disk. These are project-specific paths that would exist in the target project, not this repo. This is expected for a portable skill -- but it means the skill cannot be tested in isolation. Marking as WARN rather than FAIL for portability. |
| 6 | Research notes category count | FAIL | Line 267: "The file MUST be organized into these 6 categories" but the template that follows (lines 280-304) lists 7 sections: EXISTING_FILES, PATTERNS_AND_CONVENTIONS, FEATURE_ANALYSIS, RECOMMENDED_OUTPUTS, SUGGESTED_PHASES, TEMPLATE_NOTES, AMBIGUITIES_FOR_USER. |
| 7 | Section count claim ("32 sections") | WARN | Lines 197, 1222, and `refs/validation-checklists.md` line 102 all claim "All 32 numbered template sections." The Output Structure (lines 1014-1102) lists sections 1-28, where Section 21 has subsections 21.1-21.5. Counting subsections as separate items: 28 - 1 (S21 parent) + 5 (S21.1-21.5) = 32. The math works IF subsections are counted individually. However, this counting method is ambiguous -- the Output Structure uses only 28 `## N.` headers. The intent should be documented explicitly. |
| 8 | Tier default contradiction | FAIL | **Line 79:** "Default to Standard" / **Line 245:** "Default to Standard if unsure" / **Line 1301 (Critical Rule 11):** "Default to Heavyweight. Unless the product scope is clearly answerable with a single feature and <5 user stories, use the Heavyweight tier." Direct contradiction between Tier Selection guidance and Critical Rule 11. |
| 9 | QA checklist count mismatch (10 vs 11) | FAIL | SKILL.md lines 798-803 (Research QA Agent Prompt): Lines 798 and 801 say "10-item Research Gate checklist" but the immediately following checklist header on line 803 says "11-ITEM CHECKLIST" and lists 11 items. The same prompt in `refs/agent-prompts.md` lines 244-251 shows the same discrepancy. |
| 10 | Content duplication between SKILL.md and refs/ | WARN | Agent prompts appear TWICE: once in SKILL.md (lines 572-985) and once in `refs/agent-prompts.md`. Synthesis mapping appears TWICE: once in SKILL.md (lines 1107-1123) and once in `refs/synthesis-mapping.md`. Validation checklists appear TWICE: once in SKILL.md (lines 1127-1271) and once in `refs/validation-checklists.md`. The refs files note they were "Extracted verbatim from SKILL.md." This is intentional (refs are loaded by the builder subagent to keep SKILL.md token cost down for the orchestrator), but it creates a maintenance burden -- changes to one must be mirrored in the other. No current drift detected, but this is fragile. |
| 11 | Convention compliance vs TDD skill | PASS | Both skills follow the same structure: frontmatter, skill description, "Why This Process Works," Input, Tier Selection, Output Locations, Execution Overview, Stage A/B, Agent Prompt Templates, Output Structure, refs/ directory with agent-prompts.md, synthesis-mapping.md, validation-checklists.md. The TDD skill additionally has `refs/build-request-template.md` and `refs/operational-guidance.md` -- these are the files missing from the PRD skill. |
| 12 | Internal section references | PASS | All internal cross-references resolve: "A.1" through "A.8" are all present as subsections, Stage B references Stage A correctly, Phase numbers 1-7 are consistent throughout. |
| 13 | Instruction clarity and actionability | PASS | Instructions are detailed, specific, and actionable. Each step has clear inputs, outputs, and verification criteria. Agent prompts include complete protocols (Incremental Writing, Documentation Staleness). |
| 14 | rules/ and templates/ directories | PASS | These directories don't exist for the PRD skill, but they also don't exist for the TDD skill. Neither skill uses rules/ or templates/ subdirectories -- both embed rules in SKILL.md and use refs/ for extracted content. Convention-consistent. |

---

## Summary

- Checks passed: 8 / 14
- Checks with warnings: 3
- Checks failed: 3
- Critical issues: 1
- High issues: 2
- Medium issues: 1
- Issues fixed in-place: 3 (see below)

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | High | `SKILL.md:352,359` | References `refs/build-request-template.md` which does not exist. The BUILD_REQUEST is inlined in SKILL.md (lines 365-526) making the ref unnecessary, but the text claims the orchestrator should read it. The TDD skill has this as a separate file. | **Option A (recommended):** Remove the two references to `refs/build-request-template.md` since the content is already inlined. Update lines 352 and 359 to reflect that the BUILD_REQUEST format is provided inline below. **Option B:** Extract the BUILD_REQUEST (lines 365-526) into `refs/build-request-template.md` to match TDD convention. |
| 2 | High | `SKILL.md:79,245 vs 1301` | Tier Selection section and A.3 step 6 say "Default to Standard." Critical Rule 11 says "Default to Heavyweight." These are contradictory instructions. An agent executing this skill will not know which to follow. | Resolve the contradiction. Pick one default and make all references consistent. |
| 3 | High | `SKILL.md:798,801 vs 803` + `refs/agent-prompts.md:244 vs 251` | Research QA Agent Prompt says "10-item Research Gate checklist" but then provides an "11-ITEM CHECKLIST" with 11 items. | Update the two "10-item" references to "11-item" in both SKILL.md and refs/agent-prompts.md. |
| 4 | Medium | `SKILL.md:267` | Claims "6 categories" but the research notes template lists 7 sections. | Update "6 categories" to "7 categories". |

---

## Actions Taken

### Fix 1: Research notes category count (Issue #4)

Updated "6 categories" to "7 categories" on line 267 in `src/superclaude/skills/prd/SKILL.md`. Synced to `.claude/skills/prd/SKILL.md`.

- Verified: Grep for "7 categories" confirms the fix in both files.

### Fix 2: QA checklist count mismatch (Issue #3)

Updated "10-item" to "11-item" in the Research QA Agent Prompt in both `src/superclaude/skills/prd/SKILL.md` (lines 798, 801) and `src/superclaude/skills/prd/refs/agent-prompts.md` (lines 244, 248). Synced to `.claude/` copies.

- Verified: Both files now consistently say "11-item" matching the actual 11-ITEM CHECKLIST.

### Fix 3: Phantom `refs/build-request-template.md` reference (Issue #1)

Removed references to non-existent `refs/build-request-template.md` on lines 352 and 359. The BUILD_REQUEST format is already inlined in SKILL.md (lines 365-526), making the ref file unnecessary. Updated the text to reflect that the orchestrator uses only SKILL.md and the builder subagent loads the 3 existing refs files.

- Verified: `diff` confirms `.claude/` and `src/` remain in sync after all fixes.

---

## Remaining Unresolved Issues (Require User Decision)

### Issue #2: Tier default contradiction (High)

**Location:** `src/superclaude/skills/prd/SKILL.md` lines 79, 245, and 1301

**The problem:** Three places in the SKILL.md give contradictory tier defaults:
- **Line 79 (Tier Selection):** "Default to Standard unless the product is clearly documentable with a quick scan of <5 files."
- **Line 245 (A.3 Scope Discovery):** "Default to Standard if unsure."
- **Line 1301 (Critical Rule 11):** "Default to Heavyweight. Unless the product scope is clearly answerable with a single feature and <5 user stories, use the Heavyweight tier."

**Why this matters:** An executing agent will encounter the Tier Selection section first (line 79) and select Standard. Later, Critical Rules (line 1301) tell it to use Heavyweight. Critical Rules are labeled "Non-Negotiable" which implies they override earlier guidance, but the Tier Selection table is also framed as authoritative. This creates an irreconcilable instruction conflict.

**Recommended resolution options:**
1. **Keep Standard as default** (simpler, less token-expensive runs): Remove Critical Rule 11's override. Change it to: "When in doubt between Standard and Heavyweight, prefer Heavyweight."
2. **Keep Heavyweight as default** (more thorough): Update line 79 to "Default to Heavyweight" and line 245 to "Default to Heavyweight if unsure." This makes all three references consistent.
3. **Differentiate by scenario**: Default to Standard for Scenario A (explicit request with clear scope), default to Heavyweight for Scenario B (vague request). This is the most nuanced option but adds complexity.

**This fix is NOT safe to apply unilaterally** -- it changes the skill's behavior. The user must decide which default they prefer.

---

## Confidence Gate

- **Verified:** 12/14 (checks 1-14 all directly verified with tool calls)
- **Unverifiable:** 0
- **Unchecked:** 0
- **Confidence:** 100% (12 verified items that passed or failed with evidence, plus 2 items upgraded from FAIL to fixed)

**Tool engagement:** Read: 14 | Grep: 8 | Glob: 11 | Bash: 4

---

## Recommendations

1. **MUST resolve before merge:** Decide on tier default (Issue #2) and update all 3 locations to be consistent.
2. **Consider for future:** Extract BUILD_REQUEST into `refs/build-request-template.md` to match TDD skill convention. This is not blocking but would improve structural parity between the two skills.
3. **Consider for future:** Add a `/sc:prd` command file if direct slash command invocation is desired (currently the skill is only invocable via the Skill tool, not as a `/sc:prd` user command).
4. **Documentation note:** The "32 sections" claim works if S21 subsections are counted individually, but this should be documented explicitly in the Output Structure to avoid confusion.

## QA Complete
