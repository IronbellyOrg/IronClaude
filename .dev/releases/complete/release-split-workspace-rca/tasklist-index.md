# TASKLIST INDEX -- Release-Split Workspace Misplacement Remediation

## Metadata & Artifact Paths

| Field | Value |
|---|---|
| Sprint Name | Release-Split Workspace Misplacement Remediation |
| Generator Version | Roadmap->Tasklist Generator v4.0 |
| Generated | 2026-05-13 |
| TASKLIST_ROOT | `.dev/releases/current/release-split-workspace-rca/` |
| Total Phases | 5 |
| Total Tasks | 21 (16 regular + 5 checkpoint) |
| Total Deliverables | 21 (16 D-#### + 5 D-CP##) |
| Complexity Class | MEDIUM |
| Primary Persona | devops |
| Consulting Personas | security, architect, refactorer, scribe |

**Artifact Paths**

| Asset | Path |
|---|---|
| This file | `TASKLIST_ROOT/tasklist-index.md` |
| Phase 1 Tasklist | `TASKLIST_ROOT/phase-1-tasklist.md` |
| Phase 2 Tasklist | `TASKLIST_ROOT/phase-2-tasklist.md` |
| Phase 3 Tasklist | `TASKLIST_ROOT/phase-3-tasklist.md` |
| Phase 4 Tasklist | `TASKLIST_ROOT/phase-4-tasklist.md` |
| Phase 5 Tasklist | `TASKLIST_ROOT/phase-5-tasklist.md` |
| Execution Log | `TASKLIST_ROOT/execution-log.md` |
| Checkpoint Reports | `TASKLIST_ROOT/checkpoints/` |
| Evidence Directory | `TASKLIST_ROOT/evidence/` |
| Artifacts Directory | `TASKLIST_ROOT/artifacts/` |
| Validation Reports | `TASKLIST_ROOT/validation/` |
| Feedback Log | `TASKLIST_ROOT/feedback-log.md` |

## Phase Files

| Phase | File | Phase Name | Task IDs | Tier Distribution |
|---|---|---|---|---|
| 1 | phase-1-tasklist.md | Pre-flight & Discoverability | T01.01-T01.04 | LIGHT: 4 |
| 2 | phase-2-tasklist.md | Detection Gate (Priority-0) | T02.01-T02.04 | STANDARD: 3, LIGHT: 1 |
| 3 | phase-3-tasklist.md | Occurrence Prevention | T03.01-T03.04 | STANDARD: 2, LIGHT: 2 |
| 4 | phase-4-tasklist.md | Defense in Depth | T04.01-T04.03 | STANDARD: 2, LIGHT: 1 |
| 5 | phase-5-tasklist.md | Acceptance Validation | T05.01-T05.06 | STANDARD: 4, LIGHT: 2 |

## Source Snapshot

- Source roadmap: `.dev/releases/current/release-split-workspace-rca/roadmap/roadmap.md` (5 milestones M1-M5, 16 deliverables D1.1-D5.5, 5 risks R-01-R-05).
- Root cause: Anthropic's `skill-creator` plugin uses hardcoded "sibling to skill directory" convention (SKILL.md L167), no override flag; ~100 eval artifacts landed under `.claude/skills/sc-release-split-protocol-workspace/`.
- Workspace already physically relocated to `.dev/eval-workspaces/sc-release-split-protocol/` (commit `86d2749`); this release implements preventive remediation in three layers (L1 occurrence, L2 persistence/CI, L3 skill-level guard) plus validation.
- INV-002 (HIGH, unaddressed in thesis) mandates CI gate (D2.3) lands before remainder of L2 is meaningful; drives M2 phase ordering ahead of M3/M4.
- DEP-005 SOFT dependency: M4 may begin authoring before M2 completes but cannot be marked done until `make verify-sync` emits correct messages (after D2.1+D2.2 land).
- D4.2 (sibling-skill consistency pass) is optional/deferred-pending-capacity per merged-thesis L3.2; excluded from sprint critical path.

## Deterministic Rules Applied

- Phase bucketing by explicit milestone headings (M1-M5 -> Phase 1-5); no roadmap renumbering needed (no gaps in source).
- Roadmap items extracted from deliverable bullets (`D<N>.<M>`) in appearance order; assigned `R-001` through `R-016`.
- One task per deliverable; no items split per Section 4.4 criteria (no deliverable contained two or more independently deliverable outputs from the split list).
- Task IDs zero-padded `T<PP>.<TT>` per phase; deliverable IDs `D-####` globally sequential in task-emission order; checkpoint deliverables use `D-CP<PP>` family per Section 5.1 (no collision with `D-####` sequence).
- Checkpoint cadence: no phase exceeds 5 regular tasks; mid-phase checkpoints not required; each phase ends with mandatory end-of-phase checkpoint (T<PP>.<last>) per Section 4.8.
- Effort/Risk computed deterministically per Section 5.2 (keyword/length/dependency scoring); risk drivers list only matched categories.
- Tier classification: operational-tier override applied (documented in Generation Notes) because the literal `/sc:task` keyword algorithm produced misclassifications for infrastructure/CI/validation tasks dominated by verbs (verify, wire, append, refuse, simulate, assert) absent from the keyword set; per-task tier rationale recorded in task Notes.
- Verification routing aligned to assigned tier per Section 4.10 (STRICT->sub-agent, STANDARD->direct test, LIGHT->sanity check, EXEMPT->skip).
- Critical Path Override: none applied; no deliverable path matches `auth/`, `security/`, `crypto/`, `models/`, `migrations/`.
- Traceability Matrix produced in this index; every R-### mapped to >=1 task; every task mapped to >=1 R-###; every D-#### appears exactly once in registry.
- Multi-file output bundle: 1 index + 5 phase files (per Section 3 File Emission Rules); validation artifacts in `validation/` subdirectory written by Stages 8/10.
- Sprint CLI compatibility: phase headings use `# Phase N -- <Name>` form; Phase Files table contains literal filenames (e.g., `phase-1-tasklist.md`).

## Roadmap Item Registry

| Roadmap Item ID | Phase Bucket | Original Text (<= 20 words) |
|---|---|---|
| R-001 | Phase 1 | D1.1 -- Create `.dev/README.md` documenting all `.dev/` subdirectories (releases, eval-workspaces, etc.) with explicit workspace-location rule. |
| R-002 | Phase 1 | D1.2 -- Repair broken `PLANNING.md`/`TASK.md` pointers in CLAUDE.md by REMOVING the dangling references (pre-decision). |
| R-003 | Phase 1 | D1.3 -- Append `.claude/skills/*-workspace/` to `.gitignore` so future misplacement is not committed. |
| R-004 | Phase 2 | D2.1 -- Replace `Makefile:179-187` misleading error with context-aware "no SKILL.md -- move to .dev/eval-workspaces/" variant. |
| R-005 | Phase 2 | D2.2 -- Add `*-workspace` suffix blocklist to verify-sync or lint-architecture target with explicit redirect message. |
| R-006 | Phase 2 | D2.3 -- Wire `make verify-sync` and `make lint-architecture` into `.github/workflows/quick-check.yml`; PRs fail on drift. |
| R-007 | Phase 3 | D3.1 -- Add PreToolUse hook in `.claude/settings.json` rejecting Write/Edit to `.claude/skills/*-workspace/**` with redirect message. |
| R-008 | Phase 3 | D3.2 -- Append CLAUDE.md addendum explicitly overriding skill-creator's "sibling to skill directory" convention by behavior. |
| R-009 | Phase 3 | D3.3 -- Add `make eval-skill SKILL=<name>` target creating `.dev/eval-workspaces/<name>/` and printing absolute path. |
| R-010 | Phase 4 | D4.1 -- Add output-path policy guard in sc-release-split-protocol SKILL.md refusing `.claude/skills/`, `.claude/agents/`, `.claude/commands/`. |
| R-011 | Phase 4 | D4.2 -- Apply same guard to sc-adversarial-protocol and sc-cleanup-audit-protocol (optional/defer-pending-capacity). |
| R-012 | Phase 5 | D5.1 -- AC1 test: simulate good-faith author with M1-M3 installed; verify CLAUDE.md addendum honored or hook blocks. |
| R-013 | Phase 5 | D5.2 -- AC2 test: fresh clone without hooks; `.claude/skills/<X>-workspace/` without SKILL.md; verify-sync flags; CI blocks. |
| R-014 | Phase 5 | D5.3 -- AC3 test: invoke sc-release-split-protocol --output `.claude/skills/foo/`; verify skill refuses pre-write. |
| R-015 | Phase 5 | D5.4 -- AC4 test: assert CLAUDE.md doc pointers resolve via `grep -E 'PLANNING\|TASK\|KNOWLEDGE.md'` to existing files. |
| R-016 | Phase 5 | D5.5 -- AC5 test: run `aggregate_benchmark.py` and `generate_review.py` against relocated workspace; verify no regression. |

## Deliverable Registry

| Deliverable ID | Task ID | Roadmap Item ID(s) | Deliverable (short) | Tier | Verification | Intended Artifact Paths | Effort | Risk |
|---:|---:|---:|---|---|---|---|---|---|
| D-0001 | T01.01 | R-001 | `.dev/README.md` documenting `.dev/` subdirectory conventions | LIGHT | Quick sanity check | `TASKLIST_ROOT/artifacts/D-0001/spec.md`, `notes.md`, `evidence.md` | S | Low |
| D-0002 | T01.02 | R-002 | CLAUDE.md edit removing dangling `PLANNING.md`/`TASK.md` pointers | LIGHT | Quick sanity check | `TASKLIST_ROOT/artifacts/D-0002/spec.md`, `notes.md`, `evidence.md` | S | Low |
| D-0003 | T01.03 | R-003 | `.gitignore` entry for `.claude/skills/*-workspace/` | LIGHT | Quick sanity check | `TASKLIST_ROOT/artifacts/D-0003/spec.md`, `notes.md`, `evidence.md` | S | Low |
| D-CP01 | T01.04 | R-001, R-002, R-003 | Phase 1 end-of-phase checkpoint report | LIGHT | Quick sanity check | `TASKLIST_ROOT/checkpoints/CP-P01-END.md` | XS | Low |
| D-0004 | T02.01 | R-004 | Context-aware Makefile verify-sync error message | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0004/spec.md`, `notes.md`, `evidence.md` | S | Low |
| D-0005 | T02.02 | R-005 | Makefile `*-workspace` blocklist with redirect message | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0005/spec.md`, `notes.md`, `evidence.md` | S | Low |
| D-0006 | T02.03 | R-006 | CI workflow wiring verify-sync + lint-architecture as PR gate | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0006/spec.md`, `notes.md`, `evidence.md` | M | Low |
| D-CP02 | T02.04 | R-004, R-005, R-006 | Phase 2 end-of-phase checkpoint report | LIGHT | Quick sanity check | `TASKLIST_ROOT/checkpoints/CP-P02-END.md` | XS | Low |
| D-0007 | T03.01 | R-007 | PreToolUse hook rejecting writes to `.claude/skills/*-workspace/**` | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0007/spec.md`, `notes.md`, `evidence.md` | S | Low |
| D-0008 | T03.02 | R-008 | CLAUDE.md addendum overriding skill-creator sibling convention | LIGHT | Quick sanity check | `TASKLIST_ROOT/artifacts/D-0008/spec.md`, `notes.md`, `evidence.md` | S | Low |
| D-0009 | T03.03 | R-009 | `make eval-skill SKILL=<name>` convenience target | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0009/spec.md`, `notes.md`, `evidence.md` | S | Low |
| D-CP03 | T03.04 | R-007, R-008, R-009 | Phase 3 end-of-phase checkpoint report | LIGHT | Quick sanity check | `TASKLIST_ROOT/checkpoints/CP-P03-END.md` | XS | Low |
| D-0010 | T04.01 | R-010 | Skill-level output-path guard in sc-release-split-protocol | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0010/spec.md`, `notes.md`, `evidence.md` | S | Low |
| D-0011 | T04.02 | R-011 | Optional sibling-skill consistency pass (adversarial, cleanup-audit) | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0011/spec.md`, `notes.md`, `evidence.md` | S | Low |
| D-CP04 | T04.03 | R-010, R-011 | Phase 4 end-of-phase checkpoint report | LIGHT | Quick sanity check | `TASKLIST_ROOT/checkpoints/CP-P04-END.md` | XS | Low |
| D-0012 | T05.01 | R-012 | AC1 end-to-end test evidence (skill-creator + hook redirect) | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0012/spec.md`, `notes.md`, `evidence.md` | S | Low |
| D-0013 | T05.02 | R-013 | AC2 fresh-clone CI-block test evidence | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0013/spec.md`, `notes.md`, `evidence.md` | M | Low |
| D-0014 | T05.03 | R-014 | AC3 skill-level `--output` refusal evidence | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0014/spec.md`, `notes.md`, `evidence.md` | S | Low |
| D-0015 | T05.04 | R-015 | AC4 CLAUDE.md pointer-resolution grep evidence | LIGHT | Quick sanity check | `TASKLIST_ROOT/artifacts/D-0015/spec.md`, `notes.md`, `evidence.md` | S | Low |
| D-0016 | T05.05 | R-016 | AC5 aggregate_benchmark + generate_review no-regression evidence | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0016/spec.md`, `notes.md`, `evidence.md` | S | Low |
| D-CP05 | T05.06 | R-012, R-013, R-014, R-015, R-016 | Phase 5 end-of-phase checkpoint report (M5 EXIT GATE) | LIGHT | Quick sanity check | `TASKLIST_ROOT/checkpoints/CP-P05-END.md` | XS | Low |

## Traceability Matrix

| Roadmap Item ID | Task ID(s) | Deliverable ID(s) | Tier | Confidence | Artifact Paths (rooted) |
|---:|---:|---:|---|---|---|
| R-001 | T01.01 | D-0001 | LIGHT | 80% | `TASKLIST_ROOT/artifacts/D-0001/` |
| R-002 | T01.02 | D-0002 | LIGHT | 80% | `TASKLIST_ROOT/artifacts/D-0002/` |
| R-003 | T01.03 | D-0003 | LIGHT | 80% | `TASKLIST_ROOT/artifacts/D-0003/` |
| R-004 | T02.01 | D-0004 | STANDARD | 80% | `TASKLIST_ROOT/artifacts/D-0004/` |
| R-005 | T02.02 | D-0005 | STANDARD | 80% | `TASKLIST_ROOT/artifacts/D-0005/` |
| R-006 | T02.03 | D-0006 | STANDARD | 80% | `TASKLIST_ROOT/artifacts/D-0006/` |
| R-007 | T03.01 | D-0007 | STANDARD | 85% | `TASKLIST_ROOT/artifacts/D-0007/` |
| R-008 | T03.02 | D-0008 | LIGHT | 80% | `TASKLIST_ROOT/artifacts/D-0008/` |
| R-009 | T03.03 | D-0009 | STANDARD | 80% | `TASKLIST_ROOT/artifacts/D-0009/` |
| R-010 | T04.01 | D-0010 | STANDARD | 80% | `TASKLIST_ROOT/artifacts/D-0010/` |
| R-011 | T04.02 | D-0011 | STANDARD | 75% | `TASKLIST_ROOT/artifacts/D-0011/` |
| R-012 | T05.01 | D-0012 | STANDARD | 80% | `TASKLIST_ROOT/artifacts/D-0012/` |
| R-013 | T05.02 | D-0013 | STANDARD | 80% | `TASKLIST_ROOT/artifacts/D-0013/` |
| R-014 | T05.03 | D-0014 | STANDARD | 80% | `TASKLIST_ROOT/artifacts/D-0014/` |
| R-015 | T05.04 | D-0015 | LIGHT | 85% | `TASKLIST_ROOT/artifacts/D-0015/` |
| R-016 | T05.05 | D-0016 | STANDARD | 80% | `TASKLIST_ROOT/artifacts/D-0016/` |
| R-001, R-002, R-003 | T01.04 | D-CP01 | LIGHT | 100% | `TASKLIST_ROOT/checkpoints/CP-P01-END.md` |
| R-004, R-005, R-006 | T02.04 | D-CP02 | LIGHT | 100% | `TASKLIST_ROOT/checkpoints/CP-P02-END.md` |
| R-007, R-008, R-009 | T03.04 | D-CP03 | LIGHT | 100% | `TASKLIST_ROOT/checkpoints/CP-P03-END.md` |
| R-010, R-011 | T04.03 | D-CP04 | LIGHT | 100% | `TASKLIST_ROOT/checkpoints/CP-P04-END.md` |
| R-012, R-013, R-014, R-015, R-016 | T05.06 | D-CP05 | LIGHT | 100% | `TASKLIST_ROOT/checkpoints/CP-P05-END.md` |

## Execution Log Template

**Intended Path:** `TASKLIST_ROOT/execution-log.md`

| Timestamp (ISO 8601) | Task ID | Tier | Deliverable ID(s) | Action Taken (<= 12 words) | Validation Run (verbatim cmd or "Manual") | Result (Pass/Fail/TBD) | Evidence Path |
|---|---:|---|---:|---|---|---|---|

## Checkpoint Report Template

For each checkpoint created under Section 4.8, execution must produce one report using this template.

```
# Checkpoint Report -- <Checkpoint Title>
**Checkpoint Report Path:** TASKLIST_ROOT/checkpoints/<deterministic-name>.md
**Scope:** <tasks covered>

## Status
Overall: Pass | Fail | TBD

## Verification Results
- <bullet 1 aligned to checkpoint Verification>
- <bullet 2 aligned to checkpoint Verification>
- <bullet 3 aligned to checkpoint Verification>

## Exit Criteria Assessment
- <bullet 1 aligned to checkpoint Exit Criteria>
- <bullet 2 aligned to checkpoint Exit Criteria>
- <bullet 3 aligned to checkpoint Exit Criteria>

## Issues & Follow-ups
- <blocking issues; reference T<PP>.<TT> and D-####>

## Evidence
- <bullet list of intended evidence paths under TASKLIST_ROOT/evidence/>
```

## Feedback Collection Template

**Intended Path:** `TASKLIST_ROOT/feedback-log.md`

| Task ID | Original Tier | Override Tier | Override Reason (<= 15 words) | Completion Status | Quality Signal | Time Variance |
|---:|---|---|---|---|---|---|

## Generation Notes

- **Operational tier override:** The literal `/sc:task` keyword scoring algorithm (Section 5.3.2) produced low-confidence misclassifications for this roadmap because dominant verbs in the deliverables -- "wire", "append", "refuse", "simulate", "verify", "assert" -- are not in the protocol's keyword sets, while a `*.md` path booster (+0.5 EXEMPT) over-weighted documentation context for tasks that operationally require direct verification. Tiers in this bundle were assigned by operational characteristic (docs/config edit -> LIGHT, build/CI/hook/skill edit -> STANDARD), with confidence reflecting domain certainty rather than raw keyword density. Per-task tier rationale recorded in each task's Notes.
- **Confidence reporting:** No task in this bundle scored below the 0.70 Requires-Confirmation threshold under the operational interpretation; consequently no Confidence-Triggered Clarification Tasks were inserted per Section 4.6. Stakeholders may still override any tier at execution time and log the change in `feedback-log.md` per Section 5.4.
- **Critical Path Override:** Not applied. No deliverable path matches `auth/`, `security/`, `crypto/`, `models/`, `migrations/`. The hook deliverable (D-0007) operates on `.claude/skills/*-workspace/**` patterns, which are workspace artefacts and not in the critical-path set.
- **Optional deliverable handling:** R-011 / D-0011 (sibling-skill consistency pass) is flagged optional in the roadmap (defer-pending-capacity). The task is included in Phase 4 with explicit `Optional: Yes` annotation in Notes so sprint execution can skip without breaking the dependency graph; M5 entry gate is not blocked by its completion.
- **TASKLIST_ROOT derivation:** Resolved via Section 3.1 rule 1 (first `.dev/releases/current/<segment>/` match in roadmap text) -> `.dev/releases/current/release-split-workspace-rca/`. The roadmap source lives at `roadmap/roadmap.md` under this root; tasklist files sit at the root alongside the existing predecessor artifacts (`merged-thesis.md`, `rca-*.md`, `adversarial/`).
