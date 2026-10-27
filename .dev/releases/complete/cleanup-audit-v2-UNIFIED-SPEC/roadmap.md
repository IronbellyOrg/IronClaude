---
spec_source: .dev/releases/current/v2.1-CleanupAudit-v2/cleanup-audit-v2-UNIFIED-SPEC.md
complexity_score: 0.814
adversarial: true
base_variant: opus-architect
convergence_score: 1.0
primary_persona: architect
---

## Executive Summary

This roadmap implements `sc:cleanup-audit` v2, a 5-phase read-only repository audit that replaces the structurally deficient v1 system. The v1 system produced 12 per-file profiles from 5,857 files (99.8% miss rate) and failed to implement its own spec promises (coverage tracking, checkpointing, evidence-gated classification, spot-check validation). The v2 architecture introduces domain-aware batch decomposition, a two-tier classification system (4 primaries + 14 qualifiers), hybrid static-tool/LLM dependency analysis, tiered evidence requirements, and budget-controlled graceful degradation.

The specification derives from a 4-wave adversarial merge of two independent analysis sets (Set A single-agent, Set B multi-agent), resolving 22 conflicts across 45 topics. Key architectural decisions: 5-phase pipeline with Phase 0 profiling and Phase 4 consolidation bookends (Set B, modified), 3-tier dependency detection via static tools > grep > LLM (hybrid), minimal docs audit in core flow with full docs opt-in (hybrid), and 500K default token budget (Set B, increased from 300K per flaw analysis).

All token budget estimates are **UNVALIDATED** and require empirical benchmarking before use.

## Phased Implementation Plan

### Phase 0: Enforce Existing v1 Spec (Critical Foundation)

**Goal**: Close the spec-implementation gap — implement every v1 promise before adding new capabilities.

**Deliverables**:

1. **Two-tier classification system** with backward-compatible mapping to v1's 5 categories (DELETE, CONSOLIDATE, MOVE, FLAG, KEEP → DELETE:standard, MODIFY:consolidate-with, MODIFY:move-to, MODIFY:flag, KEEP:verified/unverified)
2. **Coverage tracking** — per-tier manifest with PASS/WARN/FAIL status against targets (Tier 1: 100%, Tier 2: 90%, Tier 3: 70%, Tier 4: 50%)
3. **Checkpointing** — `progress.json` updated after every scanner batch with phase, batch counts, file counts, token usage, timestamp
4. **Evidence-gated classification** — grep proof for DELETE (result count = 0), import reference info for Tier 1-2 KEEP
5. **10% spot-check validation** — stratified random sample, re-run evidence gathering independently, report as "consistency rate" (not accuracy)

**Quality Gates**: AC1–AC6 from acceptance criteria (Section 15 of spec)

**Dependencies**: None — this is the foundation

**Estimated Effort**: UNVALIDATED — benchmark by implementing checkpointing first, then extrapolate

### Phase 1: Correctness Fixes

**Goal**: Fix known-wrong outputs and establish structured scanner output.

**Deliverables**:

1. **Credential file scanning** — priority-ordered `.env*` enumeration, real vs template pattern detection, configurable pattern list, never print credential values, include security-audit disclaimer
2. **Gitignore consistency check** — compare `git ls-files` against `.gitignore` patterns, flag tracked-despite-ignored files as `MODIFY:flag:gitignore-inconsistency`
3. **Standardized Phase 1 scanner schema** — simplified JSON schema for Haiku scanners (path, risk_tier, classification, evidence_text, credential_scan)

**Quality Gates**: AC7 (credential scanning), AC8 (gitignore check), AC11 (schema compliance)

**Dependencies**: Phase 0 complete

### Phase 2: Infrastructure — Profiling and Batch Decomposition

**Goal**: Build the Phase 0 profiler agent and domain-aware scanning infrastructure.

**Deliverables**:

1. **audit-profiler agent** (Haiku) — repository profiling, domain detection, tier assignment, static tool orchestration
2. **Dynamic batch decomposition** — domain-aware file grouping, explicit file-list assignments per scanner batch
3. **Coverage manifest** — JSON tracking total/examined/coverage per tier with PASS/WARN/FAIL status
4. **Static analysis tool integration** — detect and run `madge`, `pydeps`, `ts-prune`, `git log --diff-filter=A`, cache outputs in `phase0/static-analysis/`
5. **Monorepo detection** — workspace file detection, per-workspace treatment
6. **`.env` key-presence matrix** — cross-file key comparison for configuration drift detection
7. **Auto-config generation** — framework/port/CI detection, conservative defaults for low-confidence fields, written to audit output dir (not repo root)
8. **`--dry-run` implementation** — Phase 0 only, display cost estimates and batch manifest preview

**Quality Gates**: Manifest completeness (100% of git-tracked files assigned), AC13 (cold-start), AC19 (dry-run)

**Dependencies**: Phase 1 complete

### Phase 3: Depth — Evidence, Cross-Reference, and Docs

**Goal**: Implement the structural audit, cross-reference synthesis, and minimal docs audit.

**Deliverables**:

1. **Evidence-mandatory KEEP for Tier 1-2** — full 8-field profiles via audit-analyzer (Sonnet)
2. **File-type-specific verification rules** — test files, deploy scripts, Docker/Compose, documentation, config/env
3. **Signal-triggered depth escalation** — configurable triggers for full-file reads (credential-adjacent imports, TODO/FIXME, complex conditionals, eval/exec, large files)
4. **3-tier cross-reference synthesis** — dependency graph with confidence-tiered edges (A: static tools, B: grep, C: LLM inference), orphan detection, connectivity analysis
5. **Duplication matrices** — content hash and function overlap grouping, >70% overlap → consolidation recommendation
6. **Minimal docs audit (core flow)** — broken reference sweep with checklist output (`- [ ] filepath:line -> missing/path`), temporal artifact classification
7. **Dynamic import detection** — configurable pattern list, dynamic-only references → `KEEP:monitor`
8. **INVESTIGATE resolution** — cross-reference with graph data, upgrade where evidence sufficient
9. **Post-hoc deduplication** — group by file path, cluster by issue category, keep highest-severity
10. **Budget controls with graceful degradation** — 4-tier degradation sequence, configurable via `--degrade-priority`
11. **Directory-level assessment blocks** — for 50+ file directories: sample list, assessment label, recommendation

**Quality Gates**: AC4 (DELETE evidence), AC5 (Tier 1-2 KEEP evidence), AC12 (cross-reference graph), AC14 (broken references), AC16 (directory assessment), AC17 (INVESTIGATE cap ≤15%)

**Dependencies**: Phase 2 complete

### Phase 4: Quality, Polish, and Consolidation

**Goal**: Complete the consolidation/validation pipeline and polish user-facing features.

**Deliverables**:

1. **audit-consolidator agent** — merge all phase summaries, deduplicate across phases, generate coverage report, directory assessments, executive summary, FINAL-REPORT.md
2. **audit-validator agent** — 10% stratified spot-check, consistency rate calculation, calibration accuracy (if ground-truth files exist), warning banners for sub-threshold rates
3. **Report depth control** — `--report-depth summary|standard|detailed`
4. **Resume from checkpoint** — `--resume` flag recovers from interrupted state using progress.json
5. **Anti-lazy enforcement** — required output fields validation, evidence non-emptiness, confidence distribution anomaly detection, cross-batch consistency checks
6. **Subagent failure handling** — per-subagent timeout (120s), max 2 retries with backoff, cascading failure detection (3 consecutive → pause), minimum viable report (50%+ batches required)

**Quality Gates**: AC3 (checkpointing + resume), AC9 (budget control), AC10 (report depth), AC18 (subagent failure), AC20 (run isolation)

**Dependencies**: Phase 3 complete

### Phase 5: Extensions (Future)

**Goal**: Add opt-in advanced features building on the established v2 foundation.

**Deliverables**:

1. **Full documentation audit** (`--pass-docs`) — Set A's 5-section format: SCOPE, CONTENT_OVERLAP_GROUPS, BROKEN_REFERENCES, CLAIM_SPOT_CHECKS (3 claims/doc, binary pass/fail), TEMPORAL_ARTIFACTS with canonical archive destinations
2. **Cross-run known-issues registry** (`--known-issues`) — signature-based JSON registry, 90-day TTL, max 200 entries with LRU eviction, auto-prune stale entries, loaded as read-only consolidator context
3. **Calibration files** — use prior run results as ground-truth baseline for consistency-vs-accuracy measurement
4. **Progressive agent specialization** — evolve from generic scanners toward 6 specialized agents (profiler, scanner, analyzer, comparator, consolidator, validator)
5. **Content overlap group detection** — topic-based document clustering with canonical doc recommendations

**Dependencies**: Phase 4 complete + at least one prior audit run for calibration data

## Risk Assessment

### Critical Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| **Spec-implementation gap recurrence (R7)** | Repeats v1 failure pattern | Every spec promise has an acceptance test; traceability matrix maintained |
| **Credential value exposure (R8)** | Security breach | Scanner prompts explicitly prohibit printing values; structural test validates no credentials in output |
| **Token budget overrun (R1)** | Audit fails or produces incomplete results | `--budget` flag, graceful degradation, `--dry-run` for preview, default raised to 500K |
| **Context window filling (R17)** | Phase 3-4 cannot read prior phase output | Write-to-disk architecture, budget accounts for re-read costs |

### High Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| **Dynamic import false positives (R3)** | Actively used files recommended for deletion | Configurable pattern list; dynamic-only → KEEP:monitor (never DELETE) |
| **Monorepo scaling (R6)** | System impractical above ~10K files | Monorepo detection, per-workspace treatment, per-directory coverage tracking |
| **Phase 0 auto-config correctness (R9)** | Wrong tier assignments cascade to all phases | Config written as visible artifact, --dry-run shows config, low-confidence fields use conservative defaults |
| **LLM-on-LLM validation limitations (R10)** | False sense of accuracy | Renamed to "consistency rate," honest framing in report, calibration files recommended |
| **Implementation effort underestimate (R15)** | Schedule overrun | All estimates marked UNVALIDATED; benchmark one feature before planning sprints |

### Medium/Low Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| **LLM output schema non-compliance (R4)** | Malformed scanner output | Simplified Phase 1 Haiku schema; retry once; mark FAILED |
| **Run-to-run non-determinism (R16)** | Diff-based trend tracking unreliable | Static analysis grounding reduces variance; acknowledged in Limitations |
| **Non-English documentation (R11)** | Broken reference detection fails | UTF-8 handling required; full multilingual out of scope |
| **GFxAI over-fitting (R14)** | Audit tuned to one repo | Separate universal features from project-specific rules; all rules configurable |

## Resource Requirements

### Agent Architecture

| Agent | Model | Phase | Budget Share |
|-------|-------|-------|-------------|
| audit-profiler | Haiku | 0 | 5% |
| audit-scanner | Haiku (parallel) | 1 | 25% |
| audit-analyzer | Sonnet (parallel) | 2 | 35% |
| audit-comparator | Sonnet | 3 | 20% |
| audit-consolidator | Sonnet | 4 | 15% (shared) |
| audit-validator | Sonnet | 4 | 15% (shared) |

### Token Budget Scenarios (UNVALIDATED)

| Scenario | Budget | Expected Coverage | Estimated Runtime |
|----------|--------|------------------|------------------|
| Minimal | 100K | Tier 1-2 only | ~8 min |
| Standard | 500K | Tier 1-3, partial Tier 4 | ~20-30 min |
| Comprehensive | 800K | All tiers | ~35-45 min |
| Deep | 1.5M | All tiers + full evidence + full docs | ~60+ min |

### External Tool Dependencies (Optional)

- `madge` (JS/TS orphan detection)
- `pydeps` (Python dependency graph)
- `ts-prune` (TypeScript unused exports)
- `cargo-deps` (Rust dependency graph)
- Standard: `git`, `grep`, `find`

### CLI Flags

12 flags total: `--pass`, `--pass-docs`, `--batch-size`, `--focus`, `--budget`, `--report-depth`, `--tier`, `--resume`, `--config`, `--dry-run`, `--known-issues`, `--degrade-priority`

## Success Criteria and Validation Approach

### Acceptance Criteria Summary

20 acceptance criteria (AC1–AC20) organized across three test tiers:

#### Tier 1: Structural Tests
- Output files exist in expected directory structure
- JSON outputs are valid and parse correctly
- FINAL-REPORT.md contains all required sections
- Schema fields are populated per phase schema definitions

#### Tier 2: Property Tests
- Coverage percentages within expected ranges per tier
- No credential values appear in any output file
- All Tier 1 (Critical) files examined when budget allows
- INVESTIGATE ≤ 15% of examined files
- DELETE entries have grep evidence with result count = 0
- Tier 1-2 KEEP entries have import reference information

#### Tier 3: Benchmark Tests
- Run against 2-3 real repositories with known characteristics
- Verify known dead code files are flagged (at least one small repo, one medium, one with known dead code)
- Measure token consumption per phase against budget estimates
- Validate graceful degradation at budget boundaries

### Key Success Metrics

| Metric | v1 Baseline | v2 Target |
|--------|------------|-----------|
| Files individually profiled | 12 / 5,857 | Budget-relative (not raw count) |
| Coverage tracking | None | Per-tier manifest with PASS/WARN/FAIL |
| Cross-boundary detection | None | 3-tier dependency analysis with confidence labels |
| Credential scanning correctness | Wrong (false negatives) | Correct (read actual content, pattern-match) |
| Classification categories | 3 | 4 primary + 14 qualifiers |
| Checkpointing | None | Per-batch disk persistence with --resume |
| Budget controls | None | --budget flag, 500K default, graceful degradation |
| Documentation audit | None | Minimal in core; full opt-in via --pass-docs |

### Validation Approach

1. **Pre-implementation**: `--dry-run` on target repositories validates Phase 0 profiling accuracy and budget estimates
2. **Per-phase**: Quality gates enforce inter-phase contracts (manifest completeness, schema compliance, evidence sufficiency, coverage thresholds)
3. **Post-implementation**: 10% spot-check measures consistency rate; calibration files (when available) measure accuracy against ground truth
4. **Cross-run**: Known-issues registry (Phase 5) enables trend tracking and suppression of resolved findings

## Timeline Estimates

All estimates are **UNVALIDATED**. Benchmark by implementing Phase 0 checkpointing first, then extrapolate.

| Implementation Phase | Scope | Dependencies |
|---------------------|-------|-------------|
| Phase 0 | Enforce v1 spec promises (5 deliverables) | None |
| Phase 1 | Correctness fixes (3 deliverables) | Phase 0 |
| Phase 2 | Infrastructure — profiling, batching, tools (8 deliverables) | Phase 1 |
| Phase 3 | Depth — evidence, cross-ref, docs (11 deliverables) | Phase 2 |
| Phase 4 | Quality — consolidation, validation, polish (6 deliverables) | Phase 3 |
| Phase 5 | Extensions — full docs, known-issues, calibration (5 deliverables) | Phase 4 + prior run data |

**Critical path**: Phase 0 → Phase 1 → Phase 2 → Phase 3 → Phase 4 (strictly sequential due to infrastructure dependencies).

**Risk mitigation for effort estimates**: The devil's advocate analysis demonstrated estimates may be 3-5x too low. Guard rail: implement one feature end-to-end before committing to sprint plans (R15).
