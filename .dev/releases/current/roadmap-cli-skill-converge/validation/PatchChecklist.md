# Patch Checklist
Generated: 2026-05-25T20:06:00+00:00
Total edits: 31 across 6 files

## File-by-file edit checklist

- tasklist-index.md
  - [ ] Update Deliverable Registry descriptions so regular deliverables name the actual `src/superclaude/...` source files where the roadmap requires source edits (from H1-H10).
  - [ ] Update Traceability Matrix artifact summaries to keep D-#### paths as evidence only, not primary source-change substitutes (from H1-H10).
- phase-1-tasklist.md
  - [ ] T01.01: make `src/superclaude/commands/roadmap.md` the primary deliverable and require exact `superclaude roadmap run --help` parity, including shared flags and cosmetic-remediation flags (from H1, M1, M3).
  - [ ] T01.02: make `src/superclaude/commands/validate-roadmap.md` the primary deliverable and require frontmatter, usage, flags, examples, output path, NFR-006, and N≥2 adversarial-merge behavior (from H2, M2).
  - [ ] T01.02: remove the direct dependency on T01.01 and keep batch sequencing at phase level (from M16).
  - [ ] T01.03: change Roadmap Item IDs to `R-001, R-002`; verify actual source files, not only artifacts; state checkpoint report is secondary evidence (from H3, M3, M4, L1).
- phase-2-tasklist.md
  - [ ] T02.01: make `src/superclaude/skills/sc-roadmap-protocol/SKILL.md` the primary deliverable and require all 14 CLI step IDs, Wave mapping, inference-only thresholds, and cosmetic gate auto-remediation (from H4).
  - [ ] T02.02: make `src/superclaude/skills/sc-roadmap-protocol/refs/scoring.md` the primary deliverable and require PRD-first signals/threshold plus CLI detection function citation (from H5).
  - [ ] T02.03: make `src/superclaude/skills/sc-roadmap-protocol/refs/templates.md` the primary deliverable and require single-template CLI behavior (from H6).
  - [ ] T02.04: make `src/superclaude/skills/sc-roadmap-protocol/refs/validation.md` the primary deliverable and require `REFLECT_GATE`, `ADVERSARIAL_MERGE_GATE`, frontmatter checks, semantic checks, and non-canonical sub-agent handling (from H7, M5).
  - [ ] T02.05: make `src/superclaude/skills/sc-roadmap-protocol/refs/extraction-pipeline.md` the primary deliverable and require `build_extract_prompt` plus `build_extract_prompt_tdd` (from H8, M6).
  - [ ] T02.06: verify D-0003 through D-0007/source-change evidence rather than only D-0003, D-0005, and D-0007 (from M7).
  - [ ] T02.07: make `src/superclaude/skills/sc-roadmap-protocol/refs/adversarial-integration.md` and `src/superclaude/skills/sc-roadmap-protocol/SKILL.md` the primary deliverables and require `build_debate_prompt` plus `_DEPTH_INSTRUCTIONS` (from H9, M8).
  - [ ] T02.08: verify D-0003 through D-0008/source-change evidence collectively (from M9).
- phase-3-tasklist.md
  - [ ] T03.01: make `src/superclaude/skills/sc-validate-roadmap-protocol/SKILL.md` the primary deliverable and require Relationship to CLI header, inference-only disclaimer, reflect/adversarial-merge CLI flow, 7/9 dimensions, and usage distinction (from H10, M10, M11).
  - [ ] T03.01: change verification method to manual source inspection plus release-level sync/regression later (from L2).
- phase-4-tasklist.md
  - [ ] T04.02: add verification/acceptance that D-0010 records the B-10 revisit condition exactly: revisit only if B-9 follow-up review finds measured load or token pain (from M12).
- phase-5-tasklist.md
  - [ ] T05.01: add three-way parity evidence for both command files across `src/`, repo-local `.claude/`, and `/config/.claude/` after global refresh (from M13).
  - [ ] T05.01: set MCP Requirements to `None` (from M17, L4).
  - [ ] T05.02: verify source-to-dev sync, repo-local/global command-copy refresh, and three-way parity evidence (from M14, M15).
  - [ ] T05.02: change rollback to deleting or regenerating the checkpoint report if recorded incorrectly (from L3).

## Cross-file consistency sweep

- [ ] Ensure regular deliverables distinguish actual source-file changes from supporting evidence artifacts.
- [ ] Ensure all checkpoint tasks that cover multiple roadmap items list all covered R-IDs.
- [ ] Ensure every phase still ends with an end-of-phase checkpoint and no regular task follows it.
- [ ] Ensure `TASKLIST_ROOT/artifacts/D-####/*` paths remain intended evidence paths only.
- [ ] Ensure no `.claude/` path is presented as a stageable source-of-truth edit.

---

## Precise diff plan

### 1) phase-1-tasklist.md

#### Section/heading to change
- `### T01.01 -- Mirror superclaude roadmap run flags in src/superclaude/commands/roadmap.md`

#### Planned edits

**A. Make source file primary**
Current issue: Deliverable says change plan under D-0001.
Change: Deliverable names `src/superclaude/commands/roadmap.md` as the output.
Diff intent: Replace “CLI-faithful `/sc:roadmap` command surface change plan” with “Updated `src/superclaude/commands/roadmap.md` with CLI-faithful `/sc:roadmap` command surface.”

**B. Require exact help parity**
Current issue: Acceptance names CLI-only flags only.
Change: Require exact parity with current `superclaude roadmap run --help`, shared flags, CLI-only flags, output wording, and cosmetic remediation flags.
Diff intent: Replace acceptance criteria with source-file-specific criteria.

#### Section/heading to change
- `### T01.02 -- Mirror superclaude roadmap validate flags in src/superclaude/commands/validate-roadmap.md`

#### Planned edits

**A. Make source file primary**
Current issue: Deliverable says change plan under D-0002.
Change: Deliverable names `src/superclaude/commands/validate-roadmap.md`.
Diff intent: Replace artifact-only acceptance with source-file criteria for frontmatter, usage, flags, examples, output path, NFR-006, and N≥2 adversarial merge.

**B. Remove over-constrained dependency**
Current issue: `Dependencies: T01.01`.
Change: `Dependencies: None`.

#### Section/heading to change
- `### T01.03 -- Checkpoint: End of Phase 01`

#### Planned edits

**A. Cover both roadmap IDs and source files**
Current issue: R-002 only and artifact-only verification.
Change: Use `R-001, R-002`; verify both source command files and cosmetic remediation flags.
Diff intent: Update Verification and Acceptance to make `CP-P01-END.md` secondary evidence summarizing direct source validation.

### 2) phase-2-tasklist.md

#### Section/heading to change
- T02.01 through T02.05 and T02.07 regular tasks

#### Planned edits

**A. Promote source files to primary deliverables**
Current issue: Tasks can pass with only D-#### artifacts.
Change: Each task names the actual `src/superclaude/skills/...` target file(s) as primary deliverables.
Diff intent: Replace “artifact” deliverables/acceptance with source-file update criteria; keep D-#### artifacts as evidence.

**B. Add missing named implementation details**
Current issue: Generic references omit named gates/builders/debate mechanisms.
Change: Add `REFLECT_GATE`, `ADVERSARIAL_MERGE_GATE`, `build_extract_prompt`, `build_extract_prompt_tdd`, `build_debate_prompt`, and `_DEPTH_INSTRUCTIONS` where applicable.

#### Section/heading to change
- T02.06 and T02.08 checkpoints

#### Planned edits

**A. Verify full covered ranges**
Current issue: Checkpoint verification omits some covered deliverables.
Change: Verify D-0003 through D-0007 for T02.06 and D-0003 through D-0008 for T02.08, with source-change evidence.

### 3) phase-3-tasklist.md

#### Section/heading to change
- `### T03.01 -- Add Relationship to CLI header to sc-validate-roadmap-protocol/SKILL.md`

#### Planned edits

**A. Promote SKILL.md source edit**
Current issue: D-0009 crosswalk artifact is primary.
Change: `src/superclaude/skills/sc-validate-roadmap-protocol/SKILL.md` is primary; D-0009 is evidence.

**B. Add missing CLI flow and usage distinction**
Current issue: Dimensions are present but reflect/adversarial-merge and usage guidance are absent.
Change: Require Relationship to CLI to state simpler reflect + adversarial-merge flow and “deep investigative validation vs automated CI/CD gating.”

### 4) phase-4-tasklist.md

#### Section/heading to change
- `### T04.02 -- Checkpoint: End of Phase 04`

#### Planned edits

**A. Add revisit condition verification**
Current issue: B-10 revisit condition missing in checkpoint.
Change: Verify D-0010 records “revisit only if B-9 follow-up review finds measured load or token pain.”

### 5) phase-5-tasklist.md

#### Section/heading to change
- `### T05.01 -- Run source sync and release verification for B-12`

#### Planned edits

**A. Add three-way parity**
Current issue: Refresh evidence is insufficient.
Change: Require md5sum or equivalent parity for both command files across `src/`, repo-local `.claude/`, and `/config/.claude/`.

**B. Remove MCP preferences**
Current issue: Preferred MCP tools are unsupported by B-12.
Change: MCP Requirements becomes `None`.

#### Section/heading to change
- `### T05.02 -- Checkpoint: End of Phase 05`

#### Planned edits

**A. Verify sync, global refresh, and parity**
Current issue: checkpoint lacks B-12 sync/global parity verification.
Change: Add verification/acceptance for source-to-dev sync, global refresh, and three-way parity.

**B. Fix rollback text**
Current issue: read-only rollback contradicts report writing.
Change: `Rollback: Delete or regenerate TASKLIST_ROOT/checkpoints/CP-P05-END.md if checkpoint verification was recorded incorrectly.`
