# TASKLIST INDEX -- TDD Command Layer Refactor

## Metadata & Artifact Paths

| Field | Value |
|---|---|
| Sprint Name | TDD Command Layer Refactor |
| Generator Version | Roadmap->Tasklist Generator v4.0 |
| Generated | 2026-04-05 |
| TASKLIST_ROOT | .dev/releases/current/v3.66-tdd-skill-refactor-v2/ |
| Total Phases | 5 |
| Total Tasks | 24 |
| Total Deliverables | 24 |
| Complexity Class | LOW |
| Primary Persona | refactorer |
| Consulting Personas | architect, scribe |

**Artifact Paths**

| Asset | Path |
|---|---|
| This file | .dev/releases/current/v3.66-tdd-skill-refactor-v2/tasklist-index.md |
| Phase 1 Tasklist | .dev/releases/current/v3.66-tdd-skill-refactor-v2/phase-1-tasklist.md |
| Phase 2 Tasklist | .dev/releases/current/v3.66-tdd-skill-refactor-v2/phase-2-tasklist.md |
| Phase 3 Tasklist | .dev/releases/current/v3.66-tdd-skill-refactor-v2/phase-3-tasklist.md |
| Phase 4 Tasklist | .dev/releases/current/v3.66-tdd-skill-refactor-v2/phase-4-tasklist.md |
| Phase 5 Tasklist | .dev/releases/current/v3.66-tdd-skill-refactor-v2/phase-5-tasklist.md |
| Execution Log | .dev/releases/current/v3.66-tdd-skill-refactor-v2/execution-log.md |
| Checkpoint Reports | .dev/releases/current/v3.66-tdd-skill-refactor-v2/checkpoints/ |
| Evidence Directory | .dev/releases/current/v3.66-tdd-skill-refactor-v2/evidence/ |
| Artifacts Directory | .dev/releases/current/v3.66-tdd-skill-refactor-v2/artifacts/ |
| Validation Reports | .dev/releases/current/v3.66-tdd-skill-refactor-v2/validation/ |
| Feedback Log | .dev/releases/current/v3.66-tdd-skill-refactor-v2/feedback-log.md |

## Phase Files

| Phase | File | Phase Name | Task IDs | Tier Distribution |
|---|---|---|---|---|
| 1 | phase-1-tasklist.md | Preparation & Template Study | T01.01-T01.04 | EXEMPT: 4 |
| 2 | phase-2-tasklist.md | Command File Creation | T02.01-T02.03 | EXEMPT: 3 |
| 3 | phase-3-tasklist.md | Content Migration | T03.01-T03.05 | STRICT: 2, EXEMPT: 3 |
| 4 | phase-4-tasklist.md | Fidelity Verification | T04.01-T04.06 | EXEMPT: 6 |
| 5 | phase-5-tasklist.md | Sync, Evidence & Commit | T05.01-T05.06 | STANDARD: 1, EXEMPT: 5 |

## Source Snapshot

- Scope: create thin command layer for TDD skill (`commands/sc/tdd.md`) and migrate ~23 lines of interface-concern content from `SKILL.md`
- Gold-standard pattern: `commands/sc/adversarial.md` (167 lines) defines the structural template
- Complexity: LOW (0.25); 2 new files, 2 modified files, ~130 new lines, ~23 lines relocated
- Zero behavioral changes; strict layer separation between command (interface) and skill (protocol)
- Source-of-truth edits in `src/superclaude/` only; dev copies via `make sync-dev`
- Estimated: ~85 minutes unbroken execution time across 5 sequential phases

## Deterministic Rules Applied

- Phase bucketing: 5 phases from explicit `### Phase N:` headings in roadmap Section 2
- Phase numbering: contiguous 1-5, no renumbering required (source already sequential)
- Task ID scheme: `T<PP>.<TT>` zero-padded (T01.01 through T05.06)
- One task per roadmap item (no splits needed; no items contained multiple independently deliverable outputs)
- Checkpoint cadence: every 5 tasks within a phase + mandatory end-of-phase
- Clarification tasks: none required (roadmap provides all implementation specifics)
- Deliverable registry: D-0001 through D-0024 (one per task)
- Effort mapping: EFFORT_SCORE computed from text length, split status, domain keywords, dependency words
- Risk mapping: RISK_SCORE computed from security, migration, auth, performance, cross-cutting keywords
- Tier classification: keyword matching + compound phrase overrides + context boosters; priority STRICT > EXEMPT > LIGHT > STANDARD
- Verification routing: tier-based method (sub-agent for STRICT, skip for EXEMPT)
- Multi-file output: 6 files (1 index + 5 phase files)

## Roadmap Item Registry

| Roadmap Item ID | Phase Bucket | Original Text (<= 20 words) |
|---|---|---|
| R-001 | Phase 1 | Read `commands/sc/adversarial.md` -- internalize section ordering, frontmatter fields, activation pattern, boundaries format |
| R-002 | Phase 1 | Read `skills/tdd/SKILL.md` -- confirm current line count (expected: 438), locate migration blocks: Lines 48-63, Lines 82-88 |
| R-003 | Phase 1 | Read Developer Guide Section 9.3 (separation of concerns) and Section 5.10 (checklist) |
| R-004 | Phase 1 | MANDATORY: Snapshot pre-migration state before any edits -- record `wc -l` on SKILL.md, `git diff --stat` baseline |
| R-005 | Phase 2 | Create `src/superclaude/commands/tdd.md` with sections: Frontmatter, Required Input, Usage, Arguments, Options Table, Behavioral Summary, Examples, Activation, Boundaries |
| R-006 | Phase 2 | Verify line count: 100-170 lines (NFR-TDD-CMD.1, FR-TDD-CMD.1l) |
| R-007 | Phase 2 | Verify zero protocol leakage: grep for `Stage A`, `Stage B`, `rf-task-builder`, `subagent` returns 0 matches |
| R-008 | Phase 3 | Migrate prompt examples (FR-TDD-CMD.2a): Copy SKILL.md lines 48-63 (3 strong + 2 weak examples) into command |
| R-009 | Phase 3 | Migrate tier table (FR-TDD-CMD.2b): Copy SKILL.md lines 82-88 (header + 3 data rows) into command Options |
| R-010 | Phase 3 | Remove migrated content from SKILL.md: Remove lines 48-63 and tier table rows 82-88, retain selection rules 90-94 |
| R-011 | Phase 3 | Verify SKILL.md post-migration line count: 400-440 lines (NFR-TDD-CMD.3, FR-TDD-CMD.2f) |
| R-012 | Phase 3 | Verify no duplication -- grep for distinctive example strings in both files; each in exactly one |
| R-013 | Phase 4 | Migrated content presence in command: grep for 3 strong + 2 weak example distinctive strings, tier rows |
| R-014 | Phase 4 | Behavioral protocol untouched: diff SKILL.md Stage A, Stage B, critical rules, session management pre/post |
| R-015 | Phase 4 | Loading declarations untouched: diff SKILL.md Phase Loading Contract table pre/post -- zero changes |
| R-016 | Phase 4 | Refs files untouched: `git diff` on all 5 refs/ files returns empty |
| R-017 | Phase 4 | Activation correctness: grep command file for `Skill tdd` |
| R-018 | Phase 4 | Migrated content removed from SKILL.md: grep for distinctive migrated strings -- 0 matches |
| R-019 | Phase 5 | Run `make sync-dev` -- propagates `src/superclaude/commands/tdd.md` to `.claude/commands/sc/tdd.md` and SKILL.md changes |
| R-020 | Phase 5 | Run `make verify-sync` -- confirm exit code 0 (SC-12) |
| R-021 | Phase 5 | Verify both file locations exist: `src/superclaude/commands/tdd.md` and `.claude/commands/sc/tdd.md` |
| R-022 | Phase 5 | Final validation pass on dev copies (repeat key checks from Phase 4 on `.claude/` copies) |
| R-023 | Phase 5 | Conditional evidence report: produce short evidence report mapping each SC and FR/NFR to verification result |
| R-024 | Phase 5 | Commit as single atomic commit: `refactor(tdd): create command layer and migrate interface content from SKILL.md` |

## Deliverable Registry

| Deliverable ID | Task ID | Roadmap Item ID(s) | Deliverable (short) | Tier | Verification | Intended Artifact Paths | Effort | Risk |
|---:|---:|---:|---|---|---|---|---|---|
| D-0001 | T01.01 | R-001 | Template analysis notes for adversarial.md gold standard | EXEMPT | Skip verification | .dev/releases/current/v3.66-tdd-skill-refactor-v2/artifacts/D-0001/notes.md | XS | Low |
| D-0002 | T01.02 | R-002 | SKILL.md state verification with line count and migration block locations | EXEMPT | Skip verification | .dev/releases/current/v3.66-tdd-skill-refactor-v2/artifacts/D-0002/notes.md | S | Low |
| D-0003 | T01.03 | R-003 | Developer Guide reference notes for Sections 9.3 and 5.10 | EXEMPT | Skip verification | .dev/releases/current/v3.66-tdd-skill-refactor-v2/artifacts/D-0003/notes.md | XS | Low |
| D-0004 | T01.04 | R-004 | Pre-migration baseline snapshot (`wc -l`, `git diff --stat`, migration block copies) | EXEMPT | Skip verification | .dev/releases/current/v3.66-tdd-skill-refactor-v2/artifacts/D-0004/evidence.md | S | Low |
| D-0005 | T02.01 | R-005 | Command file `src/superclaude/commands/tdd.md` with all 10 required sections | EXEMPT | Skip verification | .dev/releases/current/v3.66-tdd-skill-refactor-v2/artifacts/D-0005/spec.md | S | Low |
| D-0006 | T02.02 | R-006 | Line count verification evidence (100-170 lines) | EXEMPT | Skip verification | .dev/releases/current/v3.66-tdd-skill-refactor-v2/artifacts/D-0006/evidence.md | XS | Low |
| D-0007 | T02.03 | R-007 | Zero-leakage verification evidence (grep for prohibited keywords) | EXEMPT | Skip verification | .dev/releases/current/v3.66-tdd-skill-refactor-v2/artifacts/D-0007/evidence.md | XS | Low |
| D-0008 | T03.01 | R-008 | Prompt examples (3 strong + 2 weak) migrated to command Examples section | STRICT | Sub-agent (quality-engineer) | .dev/releases/current/v3.66-tdd-skill-refactor-v2/artifacts/D-0008/spec.md | M | Medium |
| D-0009 | T03.02 | R-009 | Tier selection table migrated to command Options section | STRICT | Sub-agent (quality-engineer) | .dev/releases/current/v3.66-tdd-skill-refactor-v2/artifacts/D-0009/spec.md | M | Medium |
| D-0010 | T03.03 | R-010 | SKILL.md with migrated blocks removed, retained content intact | EXEMPT | Skip verification | .dev/releases/current/v3.66-tdd-skill-refactor-v2/artifacts/D-0010/evidence.md | M | Medium |
| D-0011 | T03.04 | R-011 | Post-migration SKILL.md line count verification (400-440 lines) | EXEMPT | Skip verification | .dev/releases/current/v3.66-tdd-skill-refactor-v2/artifacts/D-0011/evidence.md | XS | Low |
| D-0012 | T03.05 | R-012 | No-duplication verification evidence across command and SKILL.md | EXEMPT | Skip verification | .dev/releases/current/v3.66-tdd-skill-refactor-v2/artifacts/D-0012/evidence.md | XS | Low |
| D-0013 | T04.01 | R-013 | Grep evidence confirming all migrated content present in command file | EXEMPT | Skip verification | .dev/releases/current/v3.66-tdd-skill-refactor-v2/artifacts/D-0013/evidence.md | XS | Low |
| D-0014 | T04.02 | R-014 | Section-level diff evidence for Stage A, Stage B, critical rules, session management | EXEMPT | Skip verification | .dev/releases/current/v3.66-tdd-skill-refactor-v2/artifacts/D-0014/evidence.md | S | Low |
| D-0015 | T04.03 | R-015 | Diff evidence for Phase Loading Contract table (zero changes) | EXEMPT | Skip verification | .dev/releases/current/v3.66-tdd-skill-refactor-v2/artifacts/D-0015/evidence.md | XS | Low |
| D-0016 | T04.04 | R-016 | Git diff evidence for all 5 refs/ files (empty diff) | EXEMPT | Skip verification | .dev/releases/current/v3.66-tdd-skill-refactor-v2/artifacts/D-0016/evidence.md | XS | Low |
| D-0017 | T04.05 | R-017 | Grep evidence confirming `Skill tdd` in command Activation section | EXEMPT | Skip verification | .dev/releases/current/v3.66-tdd-skill-refactor-v2/artifacts/D-0017/evidence.md | XS | Low |
| D-0018 | T04.06 | R-018 | Grep evidence confirming migrated strings absent from SKILL.md | EXEMPT | Skip verification | .dev/releases/current/v3.66-tdd-skill-refactor-v2/artifacts/D-0018/evidence.md | XS | Low |
| D-0019 | T05.01 | R-019 | `make sync-dev` output confirming successful propagation | STANDARD | Direct test execution | .dev/releases/current/v3.66-tdd-skill-refactor-v2/artifacts/D-0019/evidence.md | S | Low |
| D-0020 | T05.02 | R-020 | `make verify-sync` output with exit code 0 | EXEMPT | Skip verification | .dev/releases/current/v3.66-tdd-skill-refactor-v2/artifacts/D-0020/evidence.md | XS | Low |
| D-0021 | T05.03 | R-021 | File existence verification for both canonical and dev-copy locations | EXEMPT | Skip verification | .dev/releases/current/v3.66-tdd-skill-refactor-v2/artifacts/D-0021/evidence.md | XS | Low |
| D-0022 | T05.04 | R-022 | Dev-copy validation evidence (key Phase 4 checks repeated on `.claude/` copies) | EXEMPT | Skip verification | .dev/releases/current/v3.66-tdd-skill-refactor-v2/artifacts/D-0022/evidence.md | XS | Low |
| D-0023 | T05.05 | R-023 | Evidence report mapping SC and FR/NFR requirements to verification results | EXEMPT | Skip verification | .dev/releases/current/v3.66-tdd-skill-refactor-v2/artifacts/D-0023/spec.md | S | Low |
| D-0024 | T05.06 | R-024 | Atomic commit with message `refactor(tdd): create command layer and migrate interface content` | EXEMPT | Skip verification | .dev/releases/current/v3.66-tdd-skill-refactor-v2/artifacts/D-0024/evidence.md | XS | Low |

## Traceability Matrix

| Roadmap Item ID | Task ID(s) | Deliverable ID(s) | Tier | Confidence | Artifact Paths (rooted) |
|---:|---:|---:|---|---|---|
| R-001 | T01.01 | D-0001 | EXEMPT | 95% | .dev/releases/current/v3.66-tdd-skill-refactor-v2/artifacts/D-0001/notes.md |
| R-002 | T01.02 | D-0002 | EXEMPT | 90% | .dev/releases/current/v3.66-tdd-skill-refactor-v2/artifacts/D-0002/notes.md |
| R-003 | T01.03 | D-0003 | EXEMPT | 95% | .dev/releases/current/v3.66-tdd-skill-refactor-v2/artifacts/D-0003/notes.md |
| R-004 | T01.04 | D-0004 | EXEMPT | 90% | .dev/releases/current/v3.66-tdd-skill-refactor-v2/artifacts/D-0004/evidence.md |
| R-005 | T02.01 | D-0005 | EXEMPT | 50% | .dev/releases/current/v3.66-tdd-skill-refactor-v2/artifacts/D-0005/spec.md |
| R-006 | T02.02 | D-0006 | EXEMPT | 90% | .dev/releases/current/v3.66-tdd-skill-refactor-v2/artifacts/D-0006/evidence.md |
| R-007 | T02.03 | D-0007 | EXEMPT | 90% | .dev/releases/current/v3.66-tdd-skill-refactor-v2/artifacts/D-0007/evidence.md |
| R-008 | T03.01 | D-0008 | STRICT | 42% | .dev/releases/current/v3.66-tdd-skill-refactor-v2/artifacts/D-0008/spec.md |
| R-009 | T03.02 | D-0009 | STRICT | 42% | .dev/releases/current/v3.66-tdd-skill-refactor-v2/artifacts/D-0009/spec.md |
| R-010 | T03.03 | D-0010 | EXEMPT | 50% | .dev/releases/current/v3.66-tdd-skill-refactor-v2/artifacts/D-0010/evidence.md |
| R-011 | T03.04 | D-0011 | EXEMPT | 90% | .dev/releases/current/v3.66-tdd-skill-refactor-v2/artifacts/D-0011/evidence.md |
| R-012 | T03.05 | D-0012 | EXEMPT | 90% | .dev/releases/current/v3.66-tdd-skill-refactor-v2/artifacts/D-0012/evidence.md |
| R-013 | T04.01 | D-0013 | EXEMPT | 95% | .dev/releases/current/v3.66-tdd-skill-refactor-v2/artifacts/D-0013/evidence.md |
| R-014 | T04.02 | D-0014 | EXEMPT | 95% | .dev/releases/current/v3.66-tdd-skill-refactor-v2/artifacts/D-0014/evidence.md |
| R-015 | T04.03 | D-0015 | EXEMPT | 95% | .dev/releases/current/v3.66-tdd-skill-refactor-v2/artifacts/D-0015/evidence.md |
| R-016 | T04.04 | D-0016 | EXEMPT | 95% | .dev/releases/current/v3.66-tdd-skill-refactor-v2/artifacts/D-0016/evidence.md |
| R-017 | T04.05 | D-0017 | EXEMPT | 95% | .dev/releases/current/v3.66-tdd-skill-refactor-v2/artifacts/D-0017/evidence.md |
| R-018 | T04.06 | D-0018 | EXEMPT | 95% | .dev/releases/current/v3.66-tdd-skill-refactor-v2/artifacts/D-0018/evidence.md |
| R-019 | T05.01 | D-0019 | STANDARD | 35% | .dev/releases/current/v3.66-tdd-skill-refactor-v2/artifacts/D-0019/evidence.md |
| R-020 | T05.02 | D-0020 | EXEMPT | 80% | .dev/releases/current/v3.66-tdd-skill-refactor-v2/artifacts/D-0020/evidence.md |
| R-021 | T05.03 | D-0021 | EXEMPT | 80% | .dev/releases/current/v3.66-tdd-skill-refactor-v2/artifacts/D-0021/evidence.md |
| R-022 | T05.04 | D-0022 | EXEMPT | 80% | .dev/releases/current/v3.66-tdd-skill-refactor-v2/artifacts/D-0022/evidence.md |
| R-023 | T05.05 | D-0023 | EXEMPT | 50% | .dev/releases/current/v3.66-tdd-skill-refactor-v2/artifacts/D-0023/spec.md |
| R-024 | T05.06 | D-0024 | EXEMPT | 90% | .dev/releases/current/v3.66-tdd-skill-refactor-v2/artifacts/D-0024/evidence.md |

## Execution Log Template

**Intended Path:** .dev/releases/current/v3.66-tdd-skill-refactor-v2/execution-log.md

| Timestamp (ISO 8601) | Task ID | Tier | Deliverable ID(s) | Action Taken (<= 12 words) | Validation Run (verbatim cmd or "Manual") | Result (Pass/Fail/TBD) | Evidence Path |
|---|---:|---|---:|---|---|---|---|

## Checkpoint Report Template

**Template:**

```
# Checkpoint Report -- <Checkpoint Title>
**Checkpoint Report Path:** .dev/releases/current/v3.66-tdd-skill-refactor-v2/checkpoints/<deterministic-name>.md
**Scope:** <tasks covered>
## Status
Overall: Pass | Fail | TBD
## Verification Results
- <bullet 1>
- <bullet 2>
- <bullet 3>
## Exit Criteria Assessment
- <bullet 1>
- <bullet 2>
- <bullet 3>
## Issues & Follow-ups
- <list blocking issues referencing T<PP>.<TT> and D-####>
## Evidence
- <intended evidence paths under .dev/releases/current/v3.66-tdd-skill-refactor-v2/evidence/>
```

## Feedback Collection Template

**Intended Path:** .dev/releases/current/v3.66-tdd-skill-refactor-v2/feedback-log.md

| Task ID | Original Tier | Override Tier | Override Reason (<= 15 words) | Completion Status | Quality Signal | Time Variance |
|---:|---|---|---|---|---|---|

## Generation Notes

- All 5 phases derived from explicit `### Phase N:` headings in roadmap Section 2; no default bucketing applied
- "Migration" keyword in Phase 3 tasks triggered STRICT classification via Data-category keyword match; context is markdown text relocation, not database migration -- flagged as Requires Confirmation (confidence 42%)
- `*.md` path booster applied to all tasks affecting markdown files, pushing several toward EXEMPT; low-confidence tasks flagged for confirmation
- No clarification tasks needed; roadmap provides complete implementation specifics including line numbers, file paths, and verification commands
- Complexity class LOW aligns with roadmap-stated complexity score of 0.25
- 6 of 24 tasks (25%) flagged as Requires Confirmation due to tier classification uncertainty
