# TASKLIST INDEX -- TDD Skill Refactoring

## Metadata & Artifact Paths

| Field | Value |
|---|---|
| Sprint Name | TDD Skill Refactoring |
| Generator Version | Roadmap->Tasklist Generator v4.0 |
| Generated | 2026-04-03 |
| TASKLIST_ROOT | `.dev/releases/backlog/tdd-skill-refactor/tasklist/` |
| Total Phases | 5 |
| Total Tasks | 33 |
| Total Deliverables | 33 |
| Complexity Class | MEDIUM |
| Primary Persona | refactorer |
| Consulting Personas | architect, qa, analyzer |

**Artifact Paths**

| Asset | Path |
|---|---|
| This file | `.dev/releases/backlog/tdd-skill-refactor/tasklist/tasklist-index.md` |
| Phase 1 Tasklist | `.dev/releases/backlog/tdd-skill-refactor/tasklist/phase-1-tasklist.md` |
| Phase 2 Tasklist | `.dev/releases/backlog/tdd-skill-refactor/tasklist/phase-2-tasklist.md` |
| Phase 3 Tasklist | `.dev/releases/backlog/tdd-skill-refactor/tasklist/phase-3-tasklist.md` |
| Phase 4 Tasklist | `.dev/releases/backlog/tdd-skill-refactor/tasklist/phase-4-tasklist.md` |
| Phase 5 Tasklist | `.dev/releases/backlog/tdd-skill-refactor/tasklist/phase-5-tasklist.md` |
| Execution Log | `.dev/releases/backlog/tdd-skill-refactor/tasklist/execution-log.md` |
| Checkpoint Reports | `.dev/releases/backlog/tdd-skill-refactor/tasklist/checkpoints/` |
| Evidence Directory | `.dev/releases/backlog/tdd-skill-refactor/tasklist/evidence/` |
| Artifacts Directory | `.dev/releases/backlog/tdd-skill-refactor/tasklist/artifacts/` |
| Validation Reports | `.dev/releases/backlog/tdd-skill-refactor/tasklist/validation/` |
| Feedback Log | `.dev/releases/backlog/tdd-skill-refactor/tasklist/feedback-log.md` |

---

## Phase Files

| Phase | File | Phase Name | Task IDs | Tier Distribution |
|---|---|---|---|---|
| 1 | phase-1-tasklist.md | Baseline Verification & Line-Range Anchoring | T01.01-T01.07 | STRICT: 0, STANDARD: 1, LIGHT: 0, EXEMPT: 6 |
| 2 | phase-2-tasklist.md | Content Migration: Parallel Extraction | T02.01-T02.06 | STRICT: 0, STANDARD: 5, LIGHT: 0, EXEMPT: 1 |
| 3 | phase-3-tasklist.md | BUILD_REQUEST Cross-Reference Wiring | T03.01-T03.03 | STRICT: 0, STANDARD: 1, LIGHT: 0, EXEMPT: 2 |
| 4 | phase-4-tasklist.md | SKILL.md Reduction & Phase Loading Declarations | T04.01-T04.06 | STRICT: 0, STANDARD: 3, LIGHT: 0, EXEMPT: 3 |
| 5 | phase-5-tasklist.md | Sync, Full Fidelity Gate & Acceptance | T05.01-T05.11 | STRICT: 0, STANDARD: 1, LIGHT: 0, EXEMPT: 10 |

---

## Source Snapshot

- Roadmap defines a behavior-preserving decomposition of the TDD SKILL.md (1,364 lines) into a <500-line behavioral protocol plus 5 lazily-loaded refs files
- 5 sequential phases with hard quality gates between each; no phase may begin until its predecessor's verification step passes
- The adversarial-protocol refs pattern already exists in the codebase and serves as the structural precedent
- BUILD_REQUEST cross-reference wiring (FR-TDD-R.5) is the highest-risk integration point with 6 allowlisted path updates
- Fidelity index with block-level checksum markers (first 10 / last 10 words) anchors content integrity
- Spec source: `.dev/releases/backlog/tdd-skill-refactor/tdd-refactor-spec.md` (complexity_score: 0.53, target v3.8)

---

## Deterministic Rules Applied

- Phase numbering preserved as-is (1-5) — roadmap uses explicit sequential phases with no gaps
- Task IDs assigned as `T<PP>.<TT>` zero-padded format per roadmap item appearance order within each phase
- Checkpoint cadence: every 5 tasks within a phase plus mandatory end-of-phase checkpoint
- Clarification tasks: none generated — roadmap resolves all open questions within Phase 1 tasks
- Deliverable registry: 1 deliverable per task (D-0001 through D-0033)
- Effort scoring: keyword-based with text-length modifier (Section 5.2.1)
- Risk scoring: keyword-based (Section 5.2.2) — no high-risk keywords matched; all tasks Low risk
- Tier classification: EXEMPT for read-only/verification tasks, STANDARD for file creation/modification tasks
- Verification routing: EXEMPT tasks skip verification; STANDARD tasks use direct test execution
- MCP requirements: none required — refactoring tasks are file-local operations
- Traceability: every task traces to at least one R-### roadmap item
- Multi-file output: 6 files (1 index + 5 phase files) per Sprint CLI convention

---

## Roadmap Item Registry

| Roadmap Item ID | Phase Bucket | Original Text (<= 20 words) |
|---|---|---|
| R-001 | Phase 1 | Phase 1: Baseline Verification & Line-Range Anchoring — Goal and milestone |
| R-002 | Phase 1 | Count actual SKILL.md lines — run wc -l src/superclaude/skills/tdd/SKILL.md and record the observed |
| R-003 | Phase 1 | Re-anchor fidelity index line ranges — The fidelity index uses a 1,364-line baseline. Verify every |
| R-004 | Phase 1 | Resolve OQ-5 (lines 493-536 disposition) — The fidelity index maps B13 as lines 493-510 |
| R-005 | Phase 1 | Resolve OQ-2 (operational guidance range) — Confirm lines 1246-1364 contain operational guidance content |
| R-006 | Phase 1 | Resolve OQ-4 (frontmatter coverage) — Confirm B01 (lines 1-4) covers the full YAML frontmatter |
| R-007 | Phase 1 | Document phase loading contract matrix — Transcribe the loading contract from spec Section 5.3 |
| R-008 | Phase 1 | Produce corrected fidelity index — Keep block ranges aligned to the spec baseline (1,364) |
| R-009 | Phase 1 | Verification Gate: Corrected fidelity index covers lines 1-1364 with zero unmapped content lines |
| R-010 | Phase 2 | Phase 2: Content Migration — Parallel Extraction — Create 5 refs files with verbatim content |
| R-011 | Phase 2 | Create refs/agent-prompts.md (FR-TDD-R.2) — Source: Blocks B15-B22 (lines ~537-959) |
| R-012 | Phase 2 | Create refs/validation-checklists.md (FR-TDD-R.3) — Source: Blocks B25-B28 (lines ~1106-1245) |
| R-013 | Phase 2 | Create refs/synthesis-mapping.md (FR-TDD-R.4) — Source: Blocks B23-B24 (lines ~962-1105) |
| R-014 | Phase 2 | Create refs/build-request-template.md (FR-TDD-R.5) — verbatim extract only, no path rewrites yet |
| R-015 | Phase 2 | Create refs/operational-guidance.md (Architecture Section 4.1) — Source: Blocks B29-B34 (lines ~1246-1364) |
| R-016 | Phase 2 | Post-Extraction Contract Cross-Check — verify extracted file set matches the phase loading contract |
| R-017 | Phase 2 | Verification Gate: 5/5 files exist, zero drift, checksum markers match, no sentinels |
| R-018 | Phase 3 | Phase 3: BUILD_REQUEST Cross-Reference Wiring — Apply 6 allowlisted path-reference updates |
| R-019 | Phase 3 | Apply the 6 path-reference updates per FR-TDD-R.5c and FR-TDD-R.5d cross-reference map |
| R-020 | Phase 3 | Validate all updated references resolve — verify target file exists at stated path |
| R-021 | Phase 3 | Diff BUILD_REQUEST against source — Only the 6 allowlisted changes should appear |
| R-022 | Phase 3 | Verification Gate: grep for updated references matches; grep for originals returns zero |
| R-023 | Phase 4 | Phase 4: SKILL.md Reduction & Phase Loading Declarations — Reduce to <500 lines |
| R-024 | Phase 4 | Remove migrated content blocks from SKILL.md — Block B12, B15-B22, B23-B24, B25-B28, B29-B34 |
| R-025 | Phase 4 | Insert loading declarations in SKILL.md (FR-TDD-R.6) — Stage A.7 and builder load directives |
| R-026 | Phase 4 | Insert load-point replacement markers — brief directive at each removed block location |
| R-027 | Phase 4 | Preserve all behavioral blocks — B01-B11, B13, B14 remain unchanged |
| R-028 | Phase 4 | Validate SKILL.md line count — wc -l must yield strictly < 500 |
| R-029 | Phase 4 | Validate retained content — FR-TDD-R.1b through FR-TDD-R.1e acceptance criteria |
| R-030 | Phase 4 | Verification Gate: <500 lines, behavioral blocks present, loading declarations contract-compliant |
| R-031 | Phase 5 | Phase 5: Sync, Full Fidelity Gate & Acceptance — All 14 success criteria pass |
| R-032 | Phase 5 | Run make sync-dev — Propagates src/superclaude/skills/tdd/ to .claude/skills/tdd/ |
| R-033 | Phase 5 | Run make verify-sync — Must exit 0 with zero drift (SC-4) |
| R-034 | Phase 5 | Verify dev copy refs existence — ls .claude/skills/tdd/refs/ shows all 5 files |
| R-035 | Phase 5 | Full fidelity index audit (FR-TDD-R.7) — 100% coverage, checksums, allowlisted transforms only |
| R-036 | Phase 5 | Sentinel grep test — grep for {{ and <placeholder> both return empty |
| R-037 | Phase 5 | Normalized diff policy test — only line-ending/trailing-whitespace normalization permitted |
| R-038 | Phase 5 | BUILD_REQUEST resolution test — All 6 updated references point to existing files |
| R-039 | Phase 5 | Agent prompt count audit — refs/agent-prompts.md contains all 8 named prompts |
| R-040 | Phase 5 | Token count comparison — pre-refactor vs post-refactor SKILL.md token reduction |
| R-041 | Phase 5 | Behavioral parity dry run — invoke TDD skill, verify Stage A through A.7 and Stage B |
| R-042 | Phase 5 | Command-level spec review — Run /sc:spec-panel and reflection passes on release spec |
| R-043 | Phase 5 | Final Verification Gate: All 14 success criteria pass, all 4 cross-cutting gates satisfied |

---

## Deliverable Registry

| Deliverable ID | Task ID | Roadmap Item ID(s) | Deliverable (short) | Tier | Verification | Intended Artifact Paths | Effort | Risk |
|---:|---:|---:|---|---|---|---|---|---|
| D-0001 | T01.01 | R-002 | Recorded SKILL.md line count | EXEMPT | Skip | `.dev/releases/backlog/tdd-skill-refactor/tasklist/artifacts/D-0001/evidence.md` | S | Low |
| D-0002 | T01.02 | R-003 | Re-anchored fidelity index ranges B01-B34 | EXEMPT | Skip | `.dev/releases/backlog/tdd-skill-refactor/tasklist/artifacts/D-0002/evidence.md` | S | Low |
| D-0003 | T01.03 | R-004 | OQ-5 resolution (lines 493-536 disposition) | EXEMPT | Skip | `.dev/releases/backlog/tdd-skill-refactor/tasklist/artifacts/D-0003/evidence.md` | S | Low |
| D-0004 | T01.04 | R-005 | OQ-2 resolution (operational guidance range) | EXEMPT | Skip | `.dev/releases/backlog/tdd-skill-refactor/tasklist/artifacts/D-0004/evidence.md` | S | Low |
| D-0005 | T01.05 | R-006 | OQ-4 resolution (frontmatter coverage) | EXEMPT | Skip | `.dev/releases/backlog/tdd-skill-refactor/tasklist/artifacts/D-0005/evidence.md` | XS | Low |
| D-0006 | T01.06 | R-007 | Phase loading contract matrix | EXEMPT | Skip | `.dev/releases/backlog/tdd-skill-refactor/tasklist/artifacts/D-0006/spec.md` | S | Low |
| D-0007 | T01.07 | R-008 | Corrected fidelity index (lines 1-1364) | STANDARD | Direct test | `.dev/releases/backlog/tdd-skill-refactor/tasklist/artifacts/D-0007/spec.md` | S | Low |
| D-0008 | T02.01 | R-011 | refs/agent-prompts.md (8 agent templates) | STANDARD | Direct test | `.dev/releases/backlog/tdd-skill-refactor/tasklist/artifacts/D-0008/evidence.md` | S | Low |
| D-0009 | T02.02 | R-012 | refs/validation-checklists.md (checklists verbatim) | STANDARD | Direct test | `.dev/releases/backlog/tdd-skill-refactor/tasklist/artifacts/D-0009/evidence.md` | S | Low |
| D-0010 | T02.03 | R-013 | refs/synthesis-mapping.md (mapping table) | STANDARD | Direct test | `.dev/releases/backlog/tdd-skill-refactor/tasklist/artifacts/D-0010/evidence.md` | S | Low |
| D-0011 | T02.04 | R-014 | refs/build-request-template.md (verbatim pre-wiring) | STANDARD | Direct test | `.dev/releases/backlog/tdd-skill-refactor/tasklist/artifacts/D-0011/evidence.md` | S | Low |
| D-0012 | T02.05 | R-015 | refs/operational-guidance.md (guidance verbatim) | STANDARD | Direct test | `.dev/releases/backlog/tdd-skill-refactor/tasklist/artifacts/D-0012/evidence.md` | S | Low |
| D-0013 | T02.06 | R-016 | Contract cross-check report | EXEMPT | Skip | `.dev/releases/backlog/tdd-skill-refactor/tasklist/artifacts/D-0013/evidence.md` | XS | Low |
| D-0014 | T03.01 | R-019 | Updated build-request-template.md (6 path rewrites) | STANDARD | Direct test | `.dev/releases/backlog/tdd-skill-refactor/tasklist/artifacts/D-0014/evidence.md` | S | Low |
| D-0015 | T03.02 | R-020 | Reference resolution validation report | EXEMPT | Skip | `.dev/releases/backlog/tdd-skill-refactor/tasklist/artifacts/D-0015/evidence.md` | XS | Low |
| D-0016 | T03.03 | R-021 | Block B12 diff report (6 allowlisted changes) | EXEMPT | Skip | `.dev/releases/backlog/tdd-skill-refactor/tasklist/artifacts/D-0016/evidence.md` | XS | Low |
| D-0017 | T04.01 | R-024 | Reduced SKILL.md (migrated blocks removed) | STANDARD | Direct test | `.dev/releases/backlog/tdd-skill-refactor/tasklist/artifacts/D-0017/evidence.md` | S | Low |
| D-0018 | T04.02 | R-025 | SKILL.md with loading declarations (FR-TDD-R.6) | STANDARD | Direct test | `.dev/releases/backlog/tdd-skill-refactor/tasklist/artifacts/D-0018/evidence.md` | S | Low |
| D-0019 | T04.03 | R-026 | SKILL.md with load-point replacement markers | STANDARD | Direct test | `.dev/releases/backlog/tdd-skill-refactor/tasklist/artifacts/D-0019/evidence.md` | XS | Low |
| D-0020 | T04.04 | R-027 | Behavioral blocks preservation confirmation | EXEMPT | Skip | `.dev/releases/backlog/tdd-skill-refactor/tasklist/artifacts/D-0020/evidence.md` | XS | Low |
| D-0021 | T04.05 | R-028 | Line count validation (<500) | EXEMPT | Skip | `.dev/releases/backlog/tdd-skill-refactor/tasklist/artifacts/D-0021/evidence.md` | XS | Low |
| D-0022 | T04.06 | R-029 | Retained content validation (FR-TDD-R.1b-e) | EXEMPT | Skip | `.dev/releases/backlog/tdd-skill-refactor/tasklist/artifacts/D-0022/evidence.md` | XS | Low |
| D-0023 | T05.01 | R-032 | Synced dev copies (.claude/skills/tdd/ + refs/) | STANDARD | Direct test | `.dev/releases/backlog/tdd-skill-refactor/tasklist/artifacts/D-0023/evidence.md` | XS | Low |
| D-0024 | T05.02 | R-033 | Sync verification result (zero drift) | EXEMPT | Skip | `.dev/releases/backlog/tdd-skill-refactor/tasklist/artifacts/D-0024/evidence.md` | XS | Low |
| D-0025 | T05.03 | R-034 | Dev copy refs existence confirmation (5/5) | EXEMPT | Skip | `.dev/releases/backlog/tdd-skill-refactor/tasklist/artifacts/D-0025/evidence.md` | XS | Low |
| D-0026 | T05.04 | R-035 | Fidelity index audit report (FR-TDD-R.7a-f) | EXEMPT | Skip | `.dev/releases/backlog/tdd-skill-refactor/tasklist/artifacts/D-0026/spec.md` | S | Low |
| D-0027 | T05.05 | R-036 | Sentinel grep test result (zero placeholders) | EXEMPT | Skip | `.dev/releases/backlog/tdd-skill-refactor/tasklist/artifacts/D-0027/evidence.md` | XS | Low |
| D-0028 | T05.06 | R-037 | Normalized diff policy test result | EXEMPT | Skip | `.dev/releases/backlog/tdd-skill-refactor/tasklist/artifacts/D-0028/evidence.md` | XS | Low |
| D-0029 | T05.07 | R-038 | BUILD_REQUEST resolution test result | EXEMPT | Skip | `.dev/releases/backlog/tdd-skill-refactor/tasklist/artifacts/D-0029/evidence.md` | XS | Low |
| D-0030 | T05.08 | R-039 | Agent prompt count audit (8/8) | EXEMPT | Skip | `.dev/releases/backlog/tdd-skill-refactor/tasklist/artifacts/D-0030/evidence.md` | XS | Low |
| D-0031 | T05.09 | R-040 | Token count comparison report | EXEMPT | Skip | `.dev/releases/backlog/tdd-skill-refactor/tasklist/artifacts/D-0031/evidence.md` | XS | Low |
| D-0032 | T05.10 | R-041 | Behavioral parity dry run result | EXEMPT | Skip | `.dev/releases/backlog/tdd-skill-refactor/tasklist/artifacts/D-0032/evidence.md` | S | Low |
| D-0033 | T05.11 | R-042 | Spec review result (sc:spec-panel) | EXEMPT | Skip | `.dev/releases/backlog/tdd-skill-refactor/tasklist/artifacts/D-0033/evidence.md` | XS | Low |

---

## Traceability Matrix

| Roadmap Item ID | Task ID(s) | Deliverable ID(s) | Tier | Confidence | Artifact Paths (rooted) |
|---:|---:|---:|---|---|---|
| R-002 | T01.01 | D-0001 | EXEMPT | 80% | `tasklist/artifacts/D-0001/evidence.md` |
| R-003 | T01.02 | D-0002 | EXEMPT | 80% | `tasklist/artifacts/D-0002/evidence.md` |
| R-004 | T01.03 | D-0003 | EXEMPT | 80% | `tasklist/artifacts/D-0003/evidence.md` |
| R-005 | T01.04 | D-0004 | EXEMPT | 80% | `tasklist/artifacts/D-0004/evidence.md` |
| R-006 | T01.05 | D-0005 | EXEMPT | 80% | `tasklist/artifacts/D-0005/evidence.md` |
| R-007 | T01.06 | D-0006 | EXEMPT | 70% | `tasklist/artifacts/D-0006/spec.md` |
| R-008 | T01.07 | D-0007 | STANDARD | 70% | `tasklist/artifacts/D-0007/spec.md` |
| R-011 | T02.01 | D-0008 | STANDARD | 80% | `tasklist/artifacts/D-0008/evidence.md` |
| R-012 | T02.02 | D-0009 | STANDARD | 80% | `tasklist/artifacts/D-0009/evidence.md` |
| R-013 | T02.03 | D-0010 | STANDARD | 80% | `tasklist/artifacts/D-0010/evidence.md` |
| R-014 | T02.04 | D-0011 | STANDARD | 80% | `tasklist/artifacts/D-0011/evidence.md` |
| R-015 | T02.05 | D-0012 | STANDARD | 80% | `tasklist/artifacts/D-0012/evidence.md` |
| R-016 | T02.06 | D-0013 | EXEMPT | 85% | `tasklist/artifacts/D-0013/evidence.md` |
| R-019 | T03.01 | D-0014 | STANDARD | 75% | `tasklist/artifacts/D-0014/evidence.md` |
| R-020 | T03.02 | D-0015 | EXEMPT | 85% | `tasklist/artifacts/D-0015/evidence.md` |
| R-021 | T03.03 | D-0016 | EXEMPT | 85% | `tasklist/artifacts/D-0016/evidence.md` |
| R-024 | T04.01 | D-0017 | STANDARD | 75% | `tasklist/artifacts/D-0017/evidence.md` |
| R-025 | T04.02 | D-0018 | STANDARD | 75% | `tasklist/artifacts/D-0018/evidence.md` |
| R-026 | T04.03 | D-0019 | STANDARD | 75% | `tasklist/artifacts/D-0019/evidence.md` |
| R-027 | T04.04 | D-0020 | EXEMPT | 85% | `tasklist/artifacts/D-0020/evidence.md` |
| R-028 | T04.05 | D-0021 | EXEMPT | 90% | `tasklist/artifacts/D-0021/evidence.md` |
| R-029 | T04.06 | D-0022 | EXEMPT | 85% | `tasklist/artifacts/D-0022/evidence.md` |
| R-032 | T05.01 | D-0023 | STANDARD | 70% | `tasklist/artifacts/D-0023/evidence.md` |
| R-033 | T05.02 | D-0024 | EXEMPT | 85% | `tasklist/artifacts/D-0024/evidence.md` |
| R-034 | T05.03 | D-0025 | EXEMPT | 90% | `tasklist/artifacts/D-0025/evidence.md` |
| R-035 | T05.04 | D-0026 | EXEMPT | 80% | `tasklist/artifacts/D-0026/spec.md` |
| R-036 | T05.05 | D-0027 | EXEMPT | 90% | `tasklist/artifacts/D-0027/evidence.md` |
| R-037 | T05.06 | D-0028 | EXEMPT | 85% | `tasklist/artifacts/D-0028/evidence.md` |
| R-038 | T05.07 | D-0029 | EXEMPT | 85% | `tasklist/artifacts/D-0029/evidence.md` |
| R-039 | T05.08 | D-0030 | EXEMPT | 90% | `tasklist/artifacts/D-0030/evidence.md` |
| R-040 | T05.09 | D-0031 | EXEMPT | 85% | `tasklist/artifacts/D-0031/evidence.md` |
| R-041 | T05.10 | D-0032 | EXEMPT | 70% | `tasklist/artifacts/D-0032/evidence.md` |
| R-042 | T05.11 | D-0033 | EXEMPT | 85% | `tasklist/artifacts/D-0033/evidence.md` |

---

## Execution Log Template

**Intended Path:** `.dev/releases/backlog/tdd-skill-refactor/tasklist/execution-log.md`

| Timestamp (ISO 8601) | Task ID | Tier | Deliverable ID(s) | Action Taken (<= 12 words) | Validation Run (verbatim cmd or "Manual") | Result (Pass/Fail/TBD) | Evidence Path |
|---|---:|---|---:|---|---|---|---|
| | | | | | | TBD | `.dev/releases/backlog/tdd-skill-refactor/tasklist/evidence/` |

---

## Checkpoint Report Template

**Template:**

```markdown
# Checkpoint Report -- <Checkpoint Title>
**Checkpoint Report Path:** `.dev/releases/backlog/tdd-skill-refactor/tasklist/checkpoints/<deterministic-name>.md`
**Scope:** <tasks covered>

## Status
Overall: Pass | Fail | TBD

## Verification Results
- <bullet 1 aligned to checkpoint verification>
- <bullet 2 aligned to checkpoint verification>
- <bullet 3 aligned to checkpoint verification>

## Exit Criteria Assessment
- <bullet 1 aligned to checkpoint exit criteria>
- <bullet 2 aligned to checkpoint exit criteria>
- <bullet 3 aligned to checkpoint exit criteria>

## Issues & Follow-ups
- <blocking issues referencing T<PP>.<TT> and D-####>

## Evidence
- `.dev/releases/backlog/tdd-skill-refactor/tasklist/evidence/<relevant-path>`
```

Checkpoint files for this tasklist:
- `CP-P01-T01-T05.md` — Phase 1 mid-phase (after T01.05)
- `CP-P01-END.md` — End of Phase 1
- `CP-P02-T01-T05.md` — Phase 2 mid-phase (after T02.05)
- `CP-P02-END.md` — End of Phase 2
- `CP-P03-END.md` — End of Phase 3
- `CP-P04-T01-T05.md` — Phase 4 mid-phase (after T04.05)
- `CP-P04-END.md` — End of Phase 4
- `CP-P05-T01-T05.md` — Phase 5 first checkpoint (after T05.05)
- `CP-P05-T06-T10.md` — Phase 5 second checkpoint (after T05.10)
- `CP-P05-END.md` — End of Phase 5 (final gate)

---

## Feedback Collection Template

**Intended Path:** `.dev/releases/backlog/tdd-skill-refactor/tasklist/feedback-log.md`

| Task ID | Original Tier | Override Tier | Override Reason (<= 15 words) | Completion Status | Quality Signal | Time Variance |
|---:|---|---|---|---|---|---|
| | | | | | | |

**Field definitions:**
- `Override Tier`: Leave blank if no override; else the user-selected tier
- `Override Reason`: Brief justification (e.g., "Involved auth paths", "Actually trivial")
- `Completion Status`: `clean | minor-issues | major-issues | failed`
- `Quality Signal`: `pass | partial | rework-needed`
- `Time Variance`: `under-estimate | on-target | over-estimate`

---

## Generation Notes

- TASKLIST_ROOT derived via fallback (no version token or `.dev/releases/current/` path in roadmap) — overridden by command invocation to `.dev/releases/backlog/tdd-skill-refactor/tasklist/` to colocate with roadmap source
- Spec file confirmed as TDD-format; supplementary context extracted (component inventory: 5 new refs files + 2 modified files; testing strategy: 5 unit tests + 5 integration tests + 3 manual/E2E tests)
- Supplementary TDD tasks merged with existing roadmap tasks rather than duplicated (roadmap already covers all spec requirements)
- All tasks classified as Low risk — no security/migration/compliance/auth keywords in roadmap item text
- Zero STRICT tier tasks — refactoring involves file relocation with verbatim fidelity, not security-critical code changes
- Phase dependencies are strictly sequential per roadmap design; no cross-phase task reordering was needed
