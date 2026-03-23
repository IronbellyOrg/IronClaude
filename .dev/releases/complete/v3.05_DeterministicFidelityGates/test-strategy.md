---
complexity_class: HIGH
validation_philosophy: continuous-parallel
validation_milestones: 6
work_milestones: 6
interleave_ratio: "1:1"
major_issue_policy: stop-and-fix
spec_source: deterministic-fidelity-gate-requirements.md
generated: "2026-03-20T13:59:26.557072+00:00"
generator: superclaude-roadmap-executor
---

# Test Strategy — v3.05 Deterministic Fidelity Gates

## Issue Classification

| Severity | Action | Gate Impact |
|----------|--------|-------------|
| CRITICAL | stop-and-fix immediately | Blocks current phase |
| MAJOR | stop-and-fix before next phase | Blocks next phase |
| MINOR | Track and fix in next sprint | No gate impact |
| COSMETIC | Backlog | No gate impact |

---

## 1. Validation Milestones Mapped to Roadmap Phases

| Validation Milestone | Roadmap Phase | Gate | What Gets Validated |
|---------------------|---------------|------|---------------------|
| VM-1: Parser Certified | Phase 1 (Days 1–5) | A | FR-2, FR-5 parser correctness on real specs; data model backward compat |
| VM-2: Structural Determinism Certified | Phase 2 (Days 6–12) | B | FR-1, FR-3 determinism proof (SC-1); checker independence (NFR-4) |
| VM-3: Registry Certified | Phase 3 (Days 13–18) | C | FR-6, FR-10 stable IDs, cross-run memory, backward compat for pre-v3.05 registries |
| VM-4: Semantic & Debate Certified | Phase 4 (Days 19–26) | C | FR-4, FR-4.1, FR-4.2 prompt budget (SC-6), debate determinism, severity ratio (SC-4) |
| VM-5: Convergence Certified | Phase 5 (Days 27–35) | D | FR-7, FR-7.1, FR-8 convergence (SC-2), legacy compat (SC-5), dual budget mutual exclusion |
| VM-6: Release Readiness | Phase 6 (Days 36–44) | E, F | FR-9, FR-9.1, all SC-1–SC-6, all NFR-1–NFR-7 on real artifacts |

**Ratio justification**: HIGH complexity (0.88) mandates 1:1 interleaving. Every phase produces components consumed downstream — a defect in Phase 1's parser cascades to all subsequent phases. Each validation milestone must pass its gate before the next phase begins.

---

## 2. Test Categories

### Unit Tests
Pure-function validation of individual components in isolation.

| Component | Tests | Phase |
|-----------|-------|-------|
| `spec_parser.py` — YAML extraction | Parse real frontmatter, malformed YAML → `ParseWarning` | 1 |
| `spec_parser.py` — table extraction | Markdown tables by heading path, irregular tables → warning | 1 |
| `spec_parser.py` — code block extraction | Fenced blocks with language tags, missing tags → warning | 1 |
| `spec_parser.py` — ID regex | All 5 families: `FR-\d+\.\d+`, `NFR-\d+\.\d+`, `SC-\d+`, `G-\d+`, `D\d+` | 1 |
| `spec_parser.py` — signature extraction | Python signatures from fenced blocks | 1 |
| `spec_parser.py` — threshold extraction | `< 5s`, `>= 90%`, `minimum 20` | 1 |
| `split_into_sections()` | Heading splitting, frontmatter section, preamble, round-trip fidelity | 1 |
| Each structural checker (×5) | Known mismatches → expected findings with correct severity | 2 |
| `get_severity()` | All 19 canonical rules; `KeyError` on unknown combos | 2 |
| `compute_stable_id()` | Collision-free on test corpus; deterministic | 3 |
| Registry `source_layer` default | Pre-v3.05 registries → `"structural"` default | 3 |
| Prompt budget allocation | 60/20/15/5 split; truncation order; `ValueError` on oversized template | 4 |
| Debate judge | Same scores → same verdict; tiebreak within ±0.15 → CONFIRM_HIGH | 4 |
| `reimburse_for_progress()` | Returns 0 when no progress; correct credit when progress | 5 |
| Per-patch diff-size guard | Reject >30%; partial rejection; `--allow-regeneration` override | 6 |

### Integration Tests
Cross-component interaction within module boundaries.

| Integration Scope | Tests | Phase |
|-------------------|-------|-------|
| Parser → Checker pipeline | Real spec sections → checker produces typed findings | 2 |
| Checker → Registry | Findings ingested, stable IDs computed, cross-run diff | 3 |
| Registry → Semantic layer | Prior findings summary correctly bounded (≤50), truncated oldest-first | 4 |
| Structural + Semantic → Registry | `source_layer` tags correct; split HIGH counts accurate | 4 |
| Convergence → TurnLedger | Budget guards (`can_launch`, `can_remediate`) respected; never negative | 5 |
| Legacy/convergence dispatch | `convergence_enabled=false` → no TurnLedger import; `true` → registry authoritative | 5 |
| **Dual budget mutual exclusion** | Both budget systems never active simultaneously (Risk #5 — **release blocker**) | 5 |
| Regression → Debate → Registry | 3 agents merge by stable ID; debate verdicts update registry | 5 |
| Convergence → Remediation → Convergence | `execute_remediation()` called between runs; FIXED findings persist | 6 |

### End-to-End Tests
Full pipeline execution on real artifacts via CLI.

| E2E Scenario | Success Criterion | Phase |
|-------------|-------------------|-------|
| Determinism proof | Run same spec+roadmap twice → `diff` structural output = 0 bytes | 2 (initial), 6 (final) |
| Convergence termination | Pipeline terminates ≤3 runs or halts with diagnostic | 5 (initial), 6 (final) |
| Edit preservation | Remediate → re-run → FIXED stays FIXED | 6 |
| Severity ratio | ≥70% structural findings across full run | 4 (initial), 6 (final) |
| Legacy backward compat | `convergence_enabled=false` → byte-identical to `f4d9035` output | 5 (continuous), 6 (gate) |
| Prompt size compliance | Assert fires if any prompt >30,720 bytes | 4 (initial), 6 (final) |
| Full pipeline (convergence mode) | Real spec → structural → semantic → debate → convergence → remediation → pass/halt | 6 |
| Full pipeline (legacy mode) | Real spec → legacy fidelity gate → identical to baseline | 6 |

### Acceptance Tests
Mapped directly to SC-1 through SC-6 and NFR-1 through NFR-7.

| ID | Criterion | Method | Gate |
|----|-----------|--------|------|
| SC-1 | Deterministic structural findings | Dual-run byte diff | B, F |
| SC-2 | Convergence within budget | Run counter + TurnLedger balance assertion | D, F |
| SC-3 | Edit preservation | Post-remediation registry inspection | E, F |
| SC-4 | Severity anchoring ≥70% | Finding count by `source_layer` | C, F |
| SC-5 | Legacy backward compat | Byte diff against `f4d9035` | D, F |
| SC-6 | Prompt ≤30,720 bytes | Pre-LLM-call assertion | C, F |
| NFR-1 | Determinism | Covered by SC-1 | B |
| NFR-2 | Convergence ≤3 runs | Covered by SC-2 | D |
| NFR-3 | Prompt size | Covered by SC-6 | C |
| NFR-4 | Checker independence | Parallel execution + no shared state audit | B |
| NFR-5 | Edit safety ≤30% | Per-patch diff guard test | E |
| NFR-6 | Traceability | Every finding has `rule_id` or `debate_verdict` | F |
| NFR-7 | Steps 1–7 unchanged | Integration test: legacy pipeline comparison | D, F |

---

## 3. Test-Implementation Interleaving Strategy

```
Phase 1: Implement parser + data models
  └─ VM-1: Parser validation on real spec ← Gate A must pass
Phase 2: Implement 5 checkers + severity engine
  └─ VM-2: Determinism proof (SC-1 unit) ← Gate B must pass
Phase 3: Implement registry extension + run memory
  └─ VM-3: Registry cross-run + stable IDs ← Gate C must pass
Phase 4: Implement semantic layer + debate
  └─ VM-4: Prompt budget + debate consistency ← Gate C (extended) must pass
Phase 5: Implement convergence + TurnLedger + regression
  └─ VM-5: Convergence + legacy compat ← Gate D must pass
Phase 6: Implement remediation + wire E2E + dead code removal
  └─ VM-6: All SC/NFR on real artifacts ← Gates E, F must pass
```

**1:1 ratio justification**: The complexity score (0.88) and cascading dependency chain (FR-2 → FR-1 → FR-4 → FR-7) mean a defect discovered late is exponentially more expensive. Each phase's output is a direct input to the next. Validating at every boundary catches issues at the earliest possible point.

**Continuous validation**: SC-5 (legacy compat) runs after every phase from Phase 5 onward — any change that breaks legacy mode is CRITICAL severity, stop-and-fix.

---

## 4. Risk-Based Test Prioritization

### Priority 1 — CRITICAL (test first, blocks everything downstream)

| Risk | Test | Rationale |
|------|------|-----------|
| Risk #1: Parser robustness | Parser against real `deterministic-fidelity-gate-requirements.md` — not synthetic only | FR-2 is critical path entry; every downstream phase depends on it |
| Risk #5: Dual budget overlap | Integration test: `convergence_enabled` dispatch mutual exclusion | **Release blocker** per spec. Double-charging corrupts budget accounting |
| SC-5: Legacy compat | Byte diff against `f4d9035` on every pipeline change | Breaking existing behavior is a regression |

### Priority 2 — HIGH (test early in phase, blocks phase exit)

| Risk | Test | Rationale |
|------|------|-----------|
| SC-1: Determinism | Dual-run byte diff of structural findings | Core architectural premise — if checkers aren't deterministic, convergence is meaningless |
| Risk #2: Stable ID collisions | Collision test on real deviation corpus | False "new" findings undermine run-to-run memory and convergence |
| SC-6: Prompt budget | Assert before every LLM call | Oversized prompts cause truncation or API failures |
| NFR-4: Checker independence | Parallel execution test (no shared mutable state) | Shared state would violate determinism guarantee |

### Priority 3 — MEDIUM (test within phase, informs calibration)

| Risk | Test | Rationale |
|------|------|-----------|
| Risk #4: Debate calibration | Log rubric scores; verify conservative tiebreak | Heuristic threshold — safe default but needs monitoring |
| Risk #3: Temp dir cleanup | Failure injection: kill agents mid-run, verify cleanup | Disk leak is operational, not correctness |
| Risk #7: Pre-v3.05 migration | Load old registry, verify `source_layer` defaulting | Conservative default limits blast radius |

### Priority 4 — LOW (test during integration, document decisions)

| Risk | Test | Rationale |
|------|------|-----------|
| Risk #6: Import fragility | Verify conditional import works; document migration path | One-line fix if TurnLedger moves |
| Risk #8: Pass credit asymmetry | Verify net cost of Run-1 pass = 5 turns | Intentional per spec; just verify the math |

---

## 5. Acceptance Criteria per Milestone

### VM-1: Parser Certified (Gate A)
- [ ] Parser runs on real `deterministic-fidelity-gate-requirements.md` with zero crashes
- [ ] `ParseWarning` list populated for any malformed inputs encountered
- [ ] `SpecSection` round-trip: `split → reassemble` matches original content
- [ ] All 5 ID regex families extract correctly from real spec
- [ ] YAML frontmatter, markdown tables, code blocks, signatures, thresholds all extracted
- [ ] Data model extensions (`Finding`, `RunMetadata`, `RegressionResult`, `RemediationPatch`) are backward-compatible
- [ ] Interface verification complete: `TurnLedger` API, `DeviationRegistry` surface, `convergence_enabled` default confirmed
- [ ] `fidelity.py` confirmed zero imports (deletion candidate)

### VM-2: Structural Determinism Certified (Gate B)
- [ ] All 5 checkers produce typed findings from real spec sections
- [ ] SC-1 proven: identical inputs → byte-identical findings (two runs, `diff` = 0)
- [ ] All 19 canonical severity rules exercised; `KeyError` on unknown combos
- [ ] NFR-4 proven: checkers execute in parallel without interference
- [ ] Each finding contains: dimension, rule_id, severity, spec_quote, roadmap_quote_or_MISSING, location
- [ ] Machine keys used in `mismatch_type` (no prose)

### VM-3: Registry Certified (Gate C)
- [ ] Registry tracks findings across 3 simulated runs correctly
- [ ] Stable IDs are collision-free on test corpus
- [ ] FIXED findings transition correctly when not reproduced
- [ ] Pre-v3.05 registries load with `source_layer="structural"` default
- [ ] `first_seen_run` and `last_seen_run` tracked per finding
- [ ] Run-to-run memory: max 50 prior findings, oldest-first truncation
- [ ] Fixed findings not re-reported as new
- [ ] Run metadata includes all required fields
- [ ] `ACTIVE` accepted alongside `PENDING`
- [ ] Registry resets on `spec_hash` change

### VM-4: Semantic & Debate Certified (Gate C extended)
- [ ] Semantic layer processes only non-structural dimensions
- [ ] SC-6 proven: no prompt exceeds 30,720 bytes (assertion verified)
- [ ] Prompt budget allocation matches 60/20/15/5 split
- [ ] Truncation order: prior summary → structural context → spec/roadmap
- [ ] Template >5% raises `ValueError`
- [ ] Debate produces consistent verdicts on identical inputs
- [ ] Conservative tiebreak: ±0.15 margin → CONFIRM_HIGH
- [ ] 4-criterion rubric weights: 30/25/25/20
- [ ] YAML parse failure: scores default to 0
- [ ] Token budget per finding ≤5,000 (hard cap)
- [ ] SC-4 verified: ≥70% findings from structural rules
- [ ] Prior findings from registry correctly included in semantic prompt
- [ ] All semantic findings tagged `source_layer="semantic"`

### VM-5: Convergence Certified (Gate D)
- [ ] SC-2 proven: pipeline terminates ≤3 runs or halts with diagnostic
- [ ] TurnLedger budget never goes negative without halt
- [ ] Monotonic progress on `structural_high_count` only; semantic increases → warning
- [ ] SC-5 proven: legacy mode byte-identical to `f4d9035`
- [ ] Dual budget mutual exclusion verified (Risk #5 — **release blocker**)
- [ ] `convergence_enabled=false` → no TurnLedger import or construction
- [ ] `SPEC_FIDELITY_GATE` excluded in convergence mode
- [ ] Regression detection triggers on structural HIGH increase only
- [ ] 3 parallel agents spawn, merge by stable ID, all must succeed
- [ ] Temp directory cleanup verified (try/finally + atexit)
- [ ] No git worktree artifacts
- [ ] `handle_regression()` signature matches FR-7.1 contract
- [ ] Budget constants overridable; cost/credit math correct
- [ ] Convergence result maps to `StepResult`
- [ ] Steps 1–7 and step 9 unaffected (NFR-7)

### VM-6: Release Readiness (Gates E, F)
- [ ] SC-1 through SC-6 all pass on real artifacts (E2E)
- [ ] NFR-1 through NFR-7 all verified
- [ ] Remediation produces valid `RemediationPatch` objects
- [ ] Per-patch diff-size guard: >30% rejected (or applied with warning if `--allow-regeneration`)
- [ ] Partial rejection works: valid patches applied when others rejected
- [ ] Per-file rollback: each file independent
- [ ] `fidelity.py` deleted; no remaining references
- [ ] Pipeline wiring: structural → semantic → convergence → remediation in step 8
- [ ] Legacy mode regression test passes
- [ ] No orphaned temp directories after failure simulation
- [ ] All open questions (OQ-1 through OQ-6) documented with decisions
- [ ] Post-execution cross-file coherence check runs

---

## 6. Quality Gates Between Phases

### Gate A — Parser Certified (Phase 1 → Phase 2)

**Pass criteria**: All VM-1 acceptance criteria met.

**Blocking tests**:
- Real-spec parser execution (not synthetic-only)
- `SpecSection` round-trip fidelity
- Interface verification (TurnLedger, DeviationRegistry APIs)

**Failure policy**: CRITICAL — stop-and-fix. Parser is critical path; no Phase 2 work begins until parser is proven on real input.

---

### Gate B — Structural Determinism Certified (Phase 2 → Phase 3)

**Pass criteria**: All VM-2 acceptance criteria met.

**Blocking tests**:
- SC-1: Byte-identical structural findings on dual run
- NFR-4: Parallel checker execution without interference
- All 19 severity rules exercised

**Failure policy**: CRITICAL — stop-and-fix. Non-deterministic checkers invalidate the entire architectural premise.

---

### Gate C — Registry Certified (Phase 3 → Phase 4, extended through Phase 4)

**Pass criteria**: All VM-3 acceptance criteria met (Phase 3 exit). VM-4 criteria met (Phase 4 exit).

**Blocking tests (Phase 3)**:
- Stable ID collision-free on test corpus
- Cross-run finding tracking (3 simulated runs)
- Pre-v3.05 backward compatibility

**Blocking tests (Phase 4)**:
- SC-6: Prompt size assertion
- SC-4: ≥70% structural findings
- Debate verdict consistency

**Failure policy**: MAJOR on registry issues (stop-and-fix before Phase 4). CRITICAL on prompt budget violations (blocks semantic layer deployment).

---

### Gate D — Convergence Certified (Phase 5 → Phase 6)

**Pass criteria**: All VM-5 acceptance criteria met.

**Blocking tests**:
- SC-2: Convergence ≤3 runs
- SC-5: Legacy byte-identical to `f4d9035`
- **Dual budget mutual exclusion** (Risk #5 — release blocker)
- Steps 1–7 unchanged (NFR-7)

**Failure policy**: CRITICAL on dual budget overlap or legacy regression — stop-and-fix immediately. MAJOR on convergence termination failure — stop-and-fix before Phase 6.

---

### Gate E — Remediation Safety Certified (within Phase 6)

**Pass criteria**: FR-9, FR-9.1, SC-3 pass.

**Blocking tests**:
- SC-3: FIXED findings remain FIXED after remediation
- Per-patch diff-size guard enforced
- `--allow-regeneration` flag overrides with warning
- Partial rejection: valid patches survive when siblings rejected

**Failure policy**: MAJOR — stop-and-fix before Gate F.

---

### Gate F — Release Readiness (Phase 6 exit)

**Pass criteria**: All SC-1–SC-6, all NFR-1–NFR-7 pass on real artifacts via full pipeline execution.

**Blocking tests**:
- Full E2E pipeline run in convergence mode on real spec+roadmap
- Full E2E pipeline run in legacy mode with byte-diff against baseline
- All open questions documented with explicit decisions
- Dead code (`fidelity.py`) deleted and no dangling references
- No orphaned temp directories after failure injection

**Failure policy**: CRITICAL — no release until all criteria pass. Any SC or NFR failure requires root-cause analysis and re-validation from the affected gate onward.

---

## Continuous Validation (Cross-Phase)

These tests run after every phase from their introduction onward:

| Test | Introduced | Frequency | Severity if broken |
|------|------------|-----------|-------------------|
| SC-5: Legacy compat byte-diff | Phase 5 | Every commit | CRITICAL |
| NFR-7: Steps 1–7 unchanged | Phase 5 | Every commit | CRITICAL |
| SC-1: Determinism dual-run | Phase 2 | Every phase gate | CRITICAL |
| SC-6: Prompt size assertion | Phase 4 | Every LLM call | CRITICAL (runtime) |
