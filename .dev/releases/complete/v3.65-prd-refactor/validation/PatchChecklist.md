# Patch Checklist

Generated: 2026-04-03
Total edits: 24 across 4 files

## File-by-file edit checklist

- phase-1-tasklist.md
  - [x] M1: T01.01 AC -- replace "excluding inter-block whitespace" with "zero unmapped gaps" (from finding M1)
  - [x] L1a: T01.01 -- change Verification Method from "Skip verification" to "Manual verification" (from finding L1)
  - [x] L2: T01.02 AC -- remove "Baseline timestamp recorded alongside SHA for audit trail" (from finding L2)
  - [x] L1b: T01.02 -- change Verification Method from "Skip verification" to "Manual verification" (from finding L1)
  - [x] M2: T01.03 -- add step and AC for src/superclaude/skills/prd/refs/ sync confirmation (from finding M2)
  - [x] M3: T01.03 AC -- replace "Branch is based on the HEAD commit recorded in T01.02" with "Branch is created from current HEAD at time of execution" (from finding M3)
  - [x] L3: T01.03 -- change Dependencies from "T01.02" to "None" (from finding L3)
  - [x] L4: T01.04 -- remove "Header format for refs/ files documented" from AC and steps (from finding L4)

- phase-2-tasklist.md
  - [ ] L5a: T02.01 -- optionally change Verification Method to "Diff-based fidelity check" (from finding L5) [DEFERRED: optional]
  - [ ] L5b: T02.02 -- optionally change Verification Method to "Diff-based fidelity check" (from finding L5) [DEFERRED: optional]
  - [x] L6: T02.03 Why -- change "~127 lines" to "~150 lines plus header" (from finding L6)
  - [x] M4: T02.04 AC -- tighten "plus Phase 2 reference updates" to explicitly enumerate per spec Section 12.2 (from finding M4)
  - [x] L7: T02.04 Validation -- remove grep -c criterion; keep diff-based only (from finding L7)

- phase-3-tasklist.md
  - [x] H1: T03.02 AC/Validation -- replace global refs/ grep ban with loading-declaration-scoped check (from finding H1)
  - [x] M5: T03.03 -- add clarifying note that B13 is informational (not stale) per spec Section 12.2 (from finding M5)
  - [x] M6: T03.03 Validation -- replace narrow `grep -c '".*section"'` with multiple targeted grep patterns (from finding M6)
  - [x] M7: T03.04 Step 3 -- rewrite to "append without renaming B30 filenames" (from finding M7)
  - [x] H2: T03.05 -- change Verification Method from "Skip verification" to "Direct verification (wc -l + token estimate)" (from finding H2)
  - [x] H3: T03.05 AC -- remove 3.5% overshoot cap; make token estimate advisory (from finding H3)
  - [x] M8: T03.05 AC -- replace generic "remediation plan" with specific over/under diagnostics (from finding M8)

- phase-4-tasklist.md
  - [x] M9: T04.01 -- change Verification Method from "Skip verification" to "Direct verification (diff + line-count + index reconciliation)" (from finding M9)
  - [x] L8: T04.01 AC -- remove "minus deduplicated B30 rows" parenthetical (from finding L8)
  - [x] L9: T04.01 AC -- add explicit checklist/table zero-diff criterion (from finding L9)
  - [x] H4: T04.02 -- remove criterion #12 deferral; require all 12 recorded (from finding H4)
  - [x] L10: T04.03 Rollback -- replace invented wording with neutral "Re-run make sync-dev" (from finding L10)
  - [x] L11: T04.04 -- move grep check to supplemental evidence, not required AC (from finding L11)
  - [x] L12: T04.05 AC/Validation -- change "starts with" to exact equality for commit message (from finding L12)
  - [x] L13: T04.05 AC -- replace "synced src/ counterparts" with explicit file list (from finding L13)

## Cross-file consistency sweep

- [x] All EXEMPT verification tasks (T01.01, T01.02, T03.05, T04.01, T04.02) have Verification Method changed from "Skip verification" to appropriate manual/direct method
- [x] All grep-based validation criteria use sufficiently broad patterns to catch stale references

---

## Precise diff plan

### 1) phase-1-tasklist.md

#### T01.01

**A. Fix gap criterion (M1)**
Current: "Combined line coverage of all blocks accounts for all 1,373 lines of SKILL.md (excluding inter-block whitespace)"
Change to: "Combined block line ranges account for all 1,373 lines of SKILL.md with zero unmapped gaps and zero overlaps"

**B. Fix Verification Method (L1a)**
Current: "Verification Method | Skip verification"
Change to: "Verification Method | Manual verification"

#### T01.02

**C. Remove timestamp (L2)**
Current: "Baseline timestamp recorded alongside SHA for audit trail"
Change to: Remove this acceptance criterion entirely.

**D. Fix Verification Method (L1b)**
Current: "Verification Method | Skip verification"
Change to: "Verification Method | Manual verification"

#### T01.03

**E. Add sync confirmation (M2)**
Add step: "Confirm `src/superclaude/skills/prd/refs/` will be created by `make sync-dev`"
Add AC: "`src/superclaude/skills/prd/refs/` creation via `make sync-dev` confirmed"

**F. Fix branch base (M3)**
Current: "Branch is based on the HEAD commit recorded in T01.02"
Change to: "Branch is created from current HEAD at time of execution"

**G. Fix dependency (L3)**
Current: "Dependencies: T01.02"
Change to: "Dependencies: None"

#### T01.04

**H. Remove header format (L4)**
Remove: "Header format for refs/ files documented (purpose statement, loading context)" from acceptance criteria.
Remove: "Determine what patterns to observe (file naming, cross-reference syntax, header format)" -- change to "Determine what patterns to observe (file naming, cross-reference syntax)"

### 2) phase-2-tasklist.md

#### T02.03

**I. Fix size in Why (L6)**
Current: "(lines 1108-1254, ~127 lines)"
Change to: "(lines 1108-1254, ~150 lines plus header)"

#### T02.04

**J. Tighten diff scope (M4)**
Current: "ONLY the 6 documented SKILL CONTEXT FILE path changes and Phase 2 reference updates"
Change to: "exactly the 6 documented SKILL CONTEXT FILE path changes and the Phase 2 task file reference updates documented in spec Section 12.2; zero other content changes"

**K. Remove grep criterion (L7)**
Current Validation: "`grep -c '\".*section\"' refs/build-request-template.md` returns 0 (except \"Tier Selection\" which stays in SKILL.md)"
Change to: Remove this grep line from Validation section.

### 3) phase-3-tasklist.md

#### T03.02

**L. Fix refs/ grep scope (H1)**
Current AC: "`grep 'refs/' .claude/skills/prd/SKILL.md` returns matches only within the A.7 section"
Change to: "No phases outside A.7 contain loading declarations for refs/ files. Informational refs/ mentions in other sections are permitted."

Current Validation: "`grep -n 'refs/' .claude/skills/prd/SKILL.md` shows refs/ references only in A.7 section context"
Change to: "Manual inspection confirms loading declarations (Read/Load directives) for refs/ files appear only in A.7 section"

#### T03.03

**M. Clarify B13 note (M5)**
Current Step 4: "Preserve the B13 (Stage B) informational reference as-is per spec note (explains what content was baked into task file, not a loading instruction)"
Change to: "B13 (Stage B) reference describes what was baked into the task file -- this is informational, not a stale section reference per the roadmap's intent (source: spec Section 12.2)"

**N. Broaden grep pattern (M6)**
Current Validation: "`grep -c '\".*section\"' .claude/skills/prd/SKILL.md` returns 0"
Change to: "All of the following return 0: `grep -c 'Agent Prompt Templates section'`, `grep -c 'Synthesis Mapping.*section'`, `grep -c 'Assembly Process.*section'`, `grep -c 'Validation Checklist.*section'`, `grep -c 'Content Rules.*section'`"

#### T03.04

**O. Fix naming instruction (M7)**
Current Step 3: "Append B30's 6 specific QA paths as additional rows below B05's existing table, preserving B05's naming convention `[NN]-[topic-name].md`"
Change to: "Append B30's 6 specific QA paths as additional rows below B05's existing table without renaming B30 filenames; preserve B05 existing rows and keep B30 cosmetic variant as-is"

#### T03.05

**P. Fix Verification Method (H2)**
Current: "Verification Method | Skip verification"
Change to: "Verification Method | Direct verification (wc -l + token estimate)"

**Q. Fix token overshoot (H3)**
Current AC: "Estimated token count (line count * 4.5) is approximately 2,000 (soft target; ~3.5% overshoot acceptable per OQ-1)"
Change to: "Estimated token count (line count * 4.5) is advisory; do not fail if line count is 430-500. Record estimate and note if materially above ~2,000."

**R. Fix conditional criteria (M8)**
Current AC: "If line count is outside 430-500 range, remediation plan documented"
Change to: "If >500: lowest-priority behavioral candidates for decomposition identified. If <430: explicit over-extraction verification result documented."

### 4) phase-4-tasklist.md

#### T04.01

**S. Fix Verification Method (M9)**
Current: "Verification Method | Skip verification"
Change to: "Verification Method | Direct verification (diff + line-count + index reconciliation)"

**T. Remove B30 rationale (L8)**
Current: "(original 1,373 plus ref headers ~12-20 lines, minus deduplicated B30 rows)"
Change to: "(original 1,373 lines plus ref file headers)"

**U. Add checklist/table AC (L9)**
Add acceptance criterion: "`diff` of each checklist/table artifact (refs/validation-checklists.md, refs/synthesis-mapping.md) against original shows zero content changes"

#### T04.02

**V. Remove deferral (H4)**
Current Step 4: "Tally results: all 12 must pass (check 12 -- behavioral regression -- is covered by T04.04)"
Change to: "Tally results: all 12 must pass. Criterion #12 result sourced from T04.04 E2E outcome."

Current AC: "All 12 success criteria checks produce pass results (check 12 deferred to T04.04 E2E test)"
Change to: "All 12 success criteria checks produce pass results, including criterion #12 behavioral regression"

#### T04.03

**W. Fix rollback (L10)**
Current: "Rollback: `make sync-dev` can be re-run; files in `src/` are generated copies"
Change to: "Rollback: Re-run `make sync-dev` after correcting source content"

#### T04.04

**X. Move grep to supplemental (L11)**
Current Step 6: "[VERIFICATION] Grep task file output for stale \"section\" references to SKILL.md -- expect zero matches"
Change to: "[VERIFICATION] (Supplemental) Grep task file for stale references -- informational check, not a required gate"

Current AC 4th bullet: "`grep -c 'section' <task-file>` returns 0 stale SKILL.md section references"
Change to: "(Supplemental) `grep -c 'section' <task-file>` returns 0 stale references -- informational"

#### T04.05

**Y. Fix commit message match (L12)**
Current: "git log -1 --format=\"%s\" returns commit message starting with \"refactor: decompose PRD SKILL.md\""
Change to: "git log -1 --format=\"%s\" returns exactly: \"refactor: decompose PRD SKILL.md into behavioral spine + 4 refs/ files\""

**Z. Explicit src/ file list (L13)**
Current: "1 modified file (.claude/skills/prd/SKILL.md), 4 added files (.claude/skills/prd/refs/*), synced src/ counterparts"
Change to: "Modified: `.claude/skills/prd/SKILL.md`, `src/superclaude/skills/prd/SKILL.md`. Added: `.claude/skills/prd/refs/agent-prompts.md`, `.claude/skills/prd/refs/build-request-template.md`, `.claude/skills/prd/refs/synthesis-mapping.md`, `.claude/skills/prd/refs/validation-checklists.md`, `src/superclaude/skills/prd/refs/agent-prompts.md`, `src/superclaude/skills/prd/refs/build-request-template.md`, `src/superclaude/skills/prd/refs/synthesis-mapping.md`, `src/superclaude/skills/prd/refs/validation-checklists.md`"
