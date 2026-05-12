# TASKLIST INDEX -- /sc:reflect Path-Regression Refactor (Phase 5 Final Priority Matrix)

## Metadata & Artifact Paths

| Field | Value |
|---|---|
| Sprint Name | /sc:reflect Path-Regression Refactor |
| Generator Version | Roadmap->Tasklist Generator v4.0 |
| Generated | 2026-05-07 |
| TASKLIST_ROOT | `.dev/releases/current/reflect-path-regression/tasklist/` |
| Total Phases | 4 |
| Total Tasks | 17 (14 refactors + 3 clarifications) |
| Total Deliverables | 17 |
| Complexity Class | HIGH |
| Primary Persona | refactorer |
| Consulting Personas | analyzer, qa, devops |

**Artifact Paths**

| Asset | Path |
|---|---|
| This file | `TASKLIST_ROOT/tasklist-index.md` |
| Phase 1 Tasklist | `TASKLIST_ROOT/phase-1-tasklist.md` |
| Phase 2 Tasklist | `TASKLIST_ROOT/phase-2-tasklist.md` |
| Phase 3 Tasklist | `TASKLIST_ROOT/phase-3-tasklist.md` |
| Phase 4 Tasklist | `TASKLIST_ROOT/phase-4-tasklist.md` |
| Execution Log | `TASKLIST_ROOT/execution-log.md` |
| Checkpoint Reports | `TASKLIST_ROOT/checkpoints/` |
| Evidence Directory | `TASKLIST_ROOT/evidence/` |
| Artifacts Directory | `TASKLIST_ROOT/artifacts/` |
| Validation Reports | `TASKLIST_ROOT/validation/` |
| Feedback Log | `TASKLIST_ROOT/feedback-log.md` |

## Phase Files

| Phase | File | Phase Name | Task IDs | Tier Distribution |
|---|---|---|---|---|
| 1 | phase-1-tasklist.md | Tier 1 -- Foundational Detector Trio | T01.01-T01.03 | STRICT: 1, STANDARD: 2 |
| 2 | phase-2-tasklist.md | Tier 1.5 -- Verification Add-on | T02.01 | STANDARD: 1 |
| 3 | phase-3-tasklist.md | Tier 2 -- Propagation & Discipline Layer | T03.01-T03.07 | STANDARD: 5, LIGHT: 2 |
| 4 | phase-4-tasklist.md | Tier 3 -- Deferred / Conditional | T04.01-T04.06 | STANDARD: 4, LIGHT: 2 |

## Source Snapshot

- Source roadmap: `configurations/jenkins/artifacts/rca-path-regression/phase5-final-matrix.md` (Phase 5 Final Priority Matrix, 14 refactors ranked by `Priority = 0.65 * Likelihood + 0.35 * Effectiveness`).
- Supplementary spec: `configurations/jenkins/artifacts/rca-path-regression/00-consolidated-findings.md` (RCA consolidated findings from 6-lens Phase 1 investigation).
- Bug context: `pipeline-script-phase3.1.groovy:289-297` uses container path `/opt/jenkins/artifacts/` as host SSH/SCP target instead of host path `/opt/docker/jenkins_artifacts/`; mirror file is untracked in git so no commit ever held a corrected version.
- Tier 1 trio (B1+C4+C1) covers substrate, precipitating event, standing hazard with zero overlap; Phase 4 named alternate trio {B1, A5, C1} at >=0.95 joint confidence; Phase 5 swaps A5 -> C4 for upstream prevention.
- All 14 refactors target `/sc:reflect` skill protocol; rank order is stable under both 65/35 and 70/30 likelihood weightings.

## Deterministic Rules Applied

- TASKLIST_ROOT derived from `--output` flag (priority over roadmap text scan).
- Phase buckets follow explicit "Tier" headings in the source roadmap (Tier 1 -> Phase 1, Tier 1.5 -> Phase 2, Tier 2 -> Phase 3, Tier 3 -> Phase 4); no gaps; renumbered as appearance-sequential.
- Roadmap items extracted from the 14-row Final Matrix table in DESC priority order (R-001 = Rank 1 = B1 ... R-014 = Rank 14 = A3).
- Task IDs zero-padded T<PP>.<TT>; ordering preserves matrix rank within each phase.
- Clarification Tasks inserted per Section 4.6: 3 confidence/prerequisite-triggered clarifications (T03.05 for C3 tier ambiguity, T04.02 for B5 missing fetcher, T04.04 for B2 .gitignore intent).
- Effort/Risk computed from originating roadmap item text (matrix row + tier interpretation paragraph for that cause ID) per Section 5.2.
- Tier classification per Section 5.3: keyword-driven with priority STRICT > EXEMPT > LIGHT > STANDARD on conflict; "migration" -> STRICT for C4; "comment" -> LIGHT for C3 (conflict resolved by max-score, recorded in Notes).
- Verification Method routed to tier per Section 4.10; sub-agent delegation Recommended for STRICT-tier C4 only.
- MCP requirements declared per Section 5.5; Sequential preferred for tier-classification ambiguity; no STRICT critical-path overrides (no auth/security/crypto/migrations path matches in `/sc:reflect` skill source).
- Deliverable Registry produced per Section 5.1 with 17 D-#### entries each carrying spec/notes/evidence artifact placeholders under `TASKLIST_ROOT/artifacts/D-####/`.
- Checkpoint cadence per Section 4.8: end-of-phase checkpoints in every phase; Phase 3 has additional mid-phase checkpoint after T03.05; Phase 4 has additional mid-phase checkpoint after T04.05.
- Multi-file output: 1 index + 4 phase files written; validation artifacts written by Stages 7-10.

## Roadmap Item Registry

| Roadmap Item ID | Phase Bucket | Original Text (<= 20 words) |
|---|---|---|
| R-001 | Phase 1 | B1 -- Track-state audit (canonical/mirror in `git ls-files`) -- Likelihood 0.93, Effectiveness 0.95, Priority 0.937 |
| R-002 | Phase 1 | C4 -- Migration substitution-debt audit (registered host-path migrations enumerated to zero debt) -- Priority 0.924 |
| R-003 | Phase 1 | C1 -- Path-literal duplication scan (bind-mount * literal * non-identity host/ctr) -- Priority 0.878 |
| R-004 | Phase 3 | B4 -- Read-on-demand `CLAIM_TABLE` consensus across substrates -- Priority 0.852 |
| R-005 | Phase 2 | A5 -- 3-way delta sweep (spec <-> mirror <-> live) -- Priority 0.836 (Tier 1.5 add-on per matrix) |
| R-006 | Phase 3 | A1 -- Claim extraction & re-verification (regex -> grep -> DISCREPANCY) -- Priority 0.829 |
| R-007 | Phase 3 | A4 -- `Verified by:` column enforcement on state tables -- Priority 0.794 |
| R-008 | Phase 3 | B3 -- Structural-fact harvest (bind-mounts -> MEMORIZATION_PROPOSAL) -- Priority 0.761 |
| R-009 | Phase 3 | C3 -- Stale-comment drift scan (`(path, host)` pairs vs compose) -- Priority 0.731 |
| R-010 | Phase 3 | C2 -- Heredoc context decomposition (ssh/scp prefix detection) -- Priority 0.725 |
| R-011 | Phase 4 | A2 -- Spec->file application audit (parse `+`/`-` hunks; grep target) -- Priority 0.666 |
| R-012 | Phase 4 | B5 -- Tri-source reconciliation (live <-> mirror <-> handoff) -- needs Jenkins fetcher -- Priority 0.515 |
| R-013 | Phase 4 | B2 -- `.gitignore` anchor-and-coverage check -- Priority 0.468 |
| R-014 | Phase 4 | A3 -- Tool-call no-op detector (SHA pre/post + `edit_ledger.jsonl`) -- Priority 0.323 |

## Deliverable Registry

| Deliverable ID | Task ID | Roadmap Item ID(s) | Deliverable (short) | Tier | Verification | Intended Artifact Paths | Effort | Risk |
|---:|---:|---:|---|---|---|---|---|---|
| D-0001 | T01.01 | R-001 | /sc:reflect protocol patch: Track-state audit subroutine (canonical+mirror `git ls-files`) | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0001/spec.md`, `notes.md`, `evidence.md` | M | Low |
| D-0002 | T01.02 | R-002 | /sc:reflect protocol patch + `docs/migrations/*.md` registry frontmatter for migration substitution-debt audit | STRICT | Sub-agent (quality-engineer) | `TASKLIST_ROOT/artifacts/D-0002/spec.md`, `notes.md`, `evidence.md` | M | Medium |
| D-0003 | T01.03 | R-003 | /sc:reflect protocol patch: path-literal duplication scan (bind-mount x literal x non-identity host/ctr) | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0003/spec.md`, `notes.md`, `evidence.md` | M | Low |
| D-0004 | T02.01 | R-005 | /sc:reflect protocol patch: 3-way delta sweep (spec <-> mirror <-> live) | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0004/spec.md`, `notes.md`, `evidence.md` | M | Low |
| D-0005 | T03.01 | R-004 | /sc:reflect protocol patch: read-on-demand `CLAIM_TABLE` consensus across substrates | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0005/spec.md`, `notes.md`, `evidence.md` | M | Low |
| D-0006 | T03.02 | R-006 | /sc:reflect protocol patch: claim extraction & re-verification (regex -> grep -> DISCREPANCY) | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0006/spec.md`, `notes.md`, `evidence.md` | S | Low |
| D-0007 | T03.03 | R-007 | /sc:reflect protocol patch: `Verified by:` column enforcement on state tables | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0007/spec.md`, `notes.md`, `evidence.md` | S | Low |
| D-0008 | T03.04 | R-008 | /sc:reflect protocol patch: structural-fact harvest (bind-mounts -> MEMORIZATION_PROPOSAL) | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0008/spec.md`, `notes.md`, `evidence.md` | S | Low |
| D-0009 | T03.05 | R-009 | Tier-classification decision artifact for C3 (LIGHT vs STANDARD) | LIGHT | Quick sanity check | `TASKLIST_ROOT/artifacts/D-0009/spec.md`, `notes.md`, `evidence.md` | XS | Low |
| D-0010 | T03.06 | R-009 | /sc:reflect protocol patch: stale-comment drift scan (`(path, host)` pairs vs compose) | LIGHT | Quick sanity check | `TASKLIST_ROOT/artifacts/D-0010/spec.md`, `notes.md`, `evidence.md` | S | Low |
| D-0011 | T03.07 | R-010 | /sc:reflect protocol patch: heredoc context decomposition (ssh/scp prefix detection) | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0011/spec.md`, `notes.md`, `evidence.md` | S | Low |
| D-0012 | T04.01 | R-011 | /sc:reflect protocol patch: spec->file application audit (parse `+`/`-` hunks; grep target) | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0012/spec.md`, `notes.md`, `evidence.md` | S | Low |
| D-0013 | T04.02 | R-012 | Decision artifact: B5 prerequisite (Jenkins-Script-Console fetcher availability) | LIGHT | Quick sanity check | `TASKLIST_ROOT/artifacts/D-0013/spec.md`, `notes.md`, `evidence.md` | XS | Low |
| D-0014 | T04.03 | R-012 | /sc:reflect protocol patch: tri-source reconciliation (live <-> mirror <-> handoff) | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0014/spec.md`, `notes.md`, `evidence.md` | M | Low |
| D-0015 | T04.04 | R-013 | Decision artifact: B2 .gitignore intent (design vs accident) | LIGHT | Quick sanity check | `TASKLIST_ROOT/artifacts/D-0015/spec.md`, `notes.md`, `evidence.md` | XS | Low |
| D-0016 | T04.05 | R-013 | /sc:reflect protocol patch + `.gitignore` edit: anchor-and-coverage check | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0016/spec.md`, `notes.md`, `evidence.md` | XS | Low |
| D-0017 | T04.06 | R-014 | /sc:reflect protocol patch: tool-call no-op detector (SHA pre/post + `edit_ledger.jsonl`) | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0017/spec.md`, `notes.md`, `evidence.md` | L | Low |

## Traceability Matrix

| Roadmap Item ID | Task ID(s) | Deliverable ID(s) | Tier | Confidence | Artifact Paths (rooted) |
|---:|---:|---:|---|---|---|
| R-001 | T01.01 | D-0001 | STANDARD | 75% | `TASKLIST_ROOT/artifacts/D-0001/` |
| R-002 | T01.02 | D-0002 | STRICT | 80% | `TASKLIST_ROOT/artifacts/D-0002/` |
| R-003 | T01.03 | D-0003 | STANDARD | 70% | `TASKLIST_ROOT/artifacts/D-0003/` |
| R-004 | T03.01 | D-0005 | STANDARD | 70% | `TASKLIST_ROOT/artifacts/D-0005/` |
| R-005 | T02.01 | D-0004 | STANDARD | 85% | `TASKLIST_ROOT/artifacts/D-0004/` |
| R-006 | T03.02 | D-0006 | STANDARD | 70% | `TASKLIST_ROOT/artifacts/D-0006/` |
| R-007 | T03.03 | D-0007 | STANDARD | 70% | `TASKLIST_ROOT/artifacts/D-0007/` |
| R-008 | T03.04 | D-0008 | STANDARD | 70% | `TASKLIST_ROOT/artifacts/D-0008/` |
| R-009 | T03.05, T03.06 | D-0009, D-0010 | LIGHT | 65% | `TASKLIST_ROOT/artifacts/D-0009/`, `D-0010/` |
| R-010 | T03.07 | D-0011 | STANDARD | 70% | `TASKLIST_ROOT/artifacts/D-0011/` |
| R-011 | T04.01 | D-0012 | STANDARD | 70% | `TASKLIST_ROOT/artifacts/D-0012/` |
| R-012 | T04.02, T04.03 | D-0013, D-0014 | LIGHT, STANDARD | 65%, 65% | `TASKLIST_ROOT/artifacts/D-0013/`, `D-0014/` |
| R-013 | T04.04, T04.05 | D-0015, D-0016 | LIGHT, STANDARD | 65%, 65% | `TASKLIST_ROOT/artifacts/D-0015/`, `D-0016/` |
| R-014 | T04.06 | D-0017 | STANDARD | 70% | `TASKLIST_ROOT/artifacts/D-0017/` |

## Execution Log Template

**Intended Path:** `TASKLIST_ROOT/execution-log.md`

| Timestamp (ISO 8601) | Task ID | Tier | Deliverable ID(s) | Action Taken (<= 12 words) | Validation Run (verbatim cmd or "Manual") | Result (Pass/Fail/TBD) | Evidence Path |
|---|---:|---|---:|---|---|---|---|

## Checkpoint Report Template

For each checkpoint, execution must produce one report using this template (do not fabricate contents).

**Template:**
- `# Checkpoint Report -- <Checkpoint Title>`
- `**Checkpoint Report Path:** TASKLIST_ROOT/checkpoints/<deterministic-name>.md`
- `**Scope:** <tasks covered>`
- `## Status`
  - `Overall: Pass | Fail | TBD`
- `## Verification Results` (exactly 3 bullets; align to checkpoint Verification bullets)
- `## Exit Criteria Assessment` (exactly 3 bullets; align to checkpoint Exit Criteria bullets)
- `## Issues & Follow-ups`
  - List blocking issues; reference `T<PP>.<TT>` and `D-####`
- `## Evidence`
  - Bullet list of intended evidence paths under `TASKLIST_ROOT/evidence/`

## Feedback Collection Template

**Intended Path:** `TASKLIST_ROOT/feedback-log.md`

| Task ID | Original Tier | Override Tier | Override Reason (<= 15 words) | Completion Status | Quality Signal | Time Variance |
|---:|---|---|---|---|---|---|

## Generation Notes

- Spec file (`00-consolidated-findings.md`) detected as RCA findings format, NOT TDD-format (no `## 10. Component Inventory`, no TDD frontmatter, only ~5 numbered ## sections). Per Stage 4.1a fallback rule, warning logged and generation continued with roadmap-only content. No supplementary tasks generated from `--spec`.
- Tier classification confidence is uniformly low-to-moderate (0.65-0.80) because matrix-row descriptions are noun phrases ("Track-state audit", "3-way delta sweep") that lack the explicit imperative verbs ("implement", "add", "create") that the keyword scanner expects. Stage 4 enrichment baselined confidence to 0.70 for STANDARD implementation tasks where the broader tier-interpretation paragraph confirms scope.
- C3 (T03.06) tier conflict: keyword "comment" matched LIGHT (+0.3) vs implied STANDARD implementation; LIGHT won by max-score per Section 5.3.2; recorded in T03.06 Notes. Clarification task T03.05 inserted to confirm intent before execution.
- B5 (T04.03) carries an explicit prerequisite gap (no Jenkins-Script-Console fetcher in project). Clarification task T04.02 inserted per Section 4.6 main rule.
- B2 (T04.05) is conditional on user intent for the unanchored `.gitignore` line. Clarification task T04.04 inserted per Section 4.6 main rule.
- No tasks triggered Critical Path Override: the refactors target `/sc:reflect` skill protocol files only, not `auth/`, `security/`, `crypto/`, `models/`, or `migrations/` repository paths. C4 deals with documenting host-path migrations as registry entries, not repository migration code.
- A5 (R-005) appears at matrix rank 5 but Phase 5 explicitly designates it as a Tier 1.5 "shipping order" add-on; bucketed into Phase 2 to honor the roadmap's stated execution sequence rather than its priority rank.
