# Base Selection Report: Anti-Instinct Proposals 01-05

**Pipeline**: 5-variant adversarial debate
**Timestamp**: 2026-03-17T00:00:00Z
**Scoring method**: Custom 4-dimension framework (D1-D4)
**Convergence threshold**: 0.80
**Position-bias mitigation**: Scoring grounded in diff analysis evidence (S-NNN, C-NNN, U-NNN, X-NNN, A-NNN)

---

## 1. Scoring Breakdown

### D1: Efficacy (weight 0.35)

How reliably would this catch the cli-portify bug class?

| Variant | Primary Solution | Score | Rationale |
|---------|-----------------|-------|-----------|
| V4 | Hybrid (IDs + Fingerprints + Adversarial) | 9 | Fingerprints alone at 95% confidence (diff analysis C-030 rank 1). Three layers with strongest independence argument (deterministic Layers 1-2 uncorrelated with LLM biases). |
| V1 | Defense-in-depth (A + D + E) | 8 | Three checks but independence assumption weakened by A-010 (correlated tendencies). Solution E shares LLM blindspots. Solution A depends on extraction quality (A-001). |
| V5 | Integration Contract Extractor | 8 | 90% confidence via mechanism-aware detection. DISPATCH_PATTERNS match `PROGRAMMATIC_RUNNERS`. WIRING_TASK_PATTERNS find no coverage. Clear detection. Finite pattern library caps at 8. |
| V2 | Obligation Scanner | 7 | 85% confidence. "Mocked steps" is an unambiguous scaffold term. No discharge found in later phases. Misses if scaffolding uses non-standard vocabulary. Does not catch pure omissions. |
| V3 | Coherence Graph | 6 | 75% confidence. Heuristic extraction from natural language is the weak link. Abstract roadmap language ("implement step runners") may not parse into graph nodes. Implementation of extraction functions is underspecified. |

### D2: Generalizability (weight 0.25)

Does it protect against broader failure classes? Transfer to other pipeline stages?

| Variant | Primary Solution | Score | Rationale |
|---------|-----------------|-------|-----------|
| V3 | Coherence Graph | 9 | Catches ANY cross-phase data flow gap (C-030-C-039 coverage breadth rank 1). Orphaned producers, unsatisfied consumers, disconnected pairs. Applies to roadmap, tasklist, and sprint validation. Not limited by vocabulary or mechanism type. |
| V2 | Obligation Scanner | 7 | Catches any undischarged scaffolding across any pipeline stage (C-032). Extensible vocabulary. Transfers to tasklist validation (stub API -> check later tasks). Limited to scaffolding language patterns. |
| V5 | Integration Contract Extractor | 7 | 7-category integration taxonomy (U-012) covers dispatch, registry, injection, routing. Rule engine (U-013) extensible. Limited to mechanism-type bugs. Does not catch NFR omissions or test requirement drops. |
| V1 | Defense-in-depth (A + D + E) | 7 | ID cross-ref works on any formal spec. Prompt constraint works on any generation step. LLM pass works on any roadmap. Degrades on informal specs (A-001). Upstream guard (V1-C, U-001) adds extraction-stage protection. |
| V4 | Hybrid (IDs + Fingerprints + Adversarial) | 7 | IDs cover formal specs; fingerprints cover code-heavy specs; negative-space covers any spec. Roadmap-specific; transferring to tasklist/sprint requires separate implementation. |

### D3: Implementation Complexity (weight 0.20, INVERTED)

Lower complexity = higher score.

| Variant | Primary Solution | Score | Rationale |
|---------|-----------------|-------|-----------|
| V2 | Obligation Scanner | 8 | ~200 LOC, 1 new file, 1 modified file. SemanticCheck on existing MERGE_GATE. No model changes. Single-file operation. Nearly production-ready code in proposal (C-045). |
| V5 | Integration Contract Extractor | 6 | ~250 LOC, 1 new file, 2 modified files. Requires multi-file access (spec + roadmap) -- needs executor workaround per C-063. Two pattern libraries to calibrate. |
| V1 | Defense-in-depth (A + D + E) | 5 | ~330 LOC across 4 files. A alone is simple (~100 LOC) but the full A+D+E adds prompt changes + LLM pipeline step + gate wiring. |
| V3 | Coherence Graph | 4 | ~300 LOC across 2 new + 2 modified files. Heuristic NLP extraction is the unsolved hard problem (S-003). Maps to existing infrastructure but still requires new extraction logic. |
| V4 | Hybrid (IDs + Fingerprints + Adversarial) | 4 | ~350 LOC, 2 new files, 3 modified files. Most complex primary solution. Multi-file access workaround needed (C-063). LLM pipeline step adds operational complexity. |

### D4: Determinism (weight 0.20)

Pure Python vs. LLM-dependent. Higher determinism = higher score.

| Variant | Primary Solution | Score | Rationale |
|---------|-----------------|-------|-----------|
| V2 | Obligation Scanner | 9 | Pure Python regex. Zero LLM calls. Identical results on same input. Phase splitting and component context extraction fully deterministic. |
| V5 | Integration Contract Extractor | 9 | Pure Python regex against two pattern libraries. Zero LLM calls. Mechanism classification deterministic. |
| V3 | Coherence Graph | 8 | Pure Python graph analysis after heuristic extraction. No LLM calls. Reproducible. Slight deduction for extraction heuristic fragility on varied inputs. |
| V1 | Defense-in-depth (A + D + E) | 6 | Solution A deterministic. Solution D is prompt-only (non-deterministic effect). Solution E adds LLM call (non-deterministic, shares blindspots per V4's Round 2 rebuttal). |
| V4 | Hybrid (IDs + Fingerprints + Adversarial) | 6 | Layers 1-2 deterministic. Layer 3 is LLM-dependent (adversarially reframed but still non-repeatable). Layer 4 is existing LLM check. Semi-deterministic overall. |

---

## 2. Composite Scores

Formula: `(D1 x 0.35) + (D2 x 0.25) + (D3 x 0.20) + (D4 x 0.20)`

| Rank | Variant | Primary Solution | D1 (0.35) | D2 (0.25) | D3 (0.20) | D4 (0.20) | Composite |
|------|---------|-----------------|-----------|-----------|-----------|-----------|-----------|
| 1 | **V2** | Obligation Scanner | 7 | 7 | 8 | 9 | **7.60** |
| 2 | **V5** | Integration Contract Extractor | 8 | 7 | 6 | 9 | **7.55** |
| 3 | V4 | Hybrid (IDs + Fingerprints + Adversarial) | 9 | 7 | 4 | 6 | 6.90 |
| 4 | V1 | Defense-in-depth (A + D + E) | 8 | 7 | 5 | 6 | 6.75 |
| 5 | V3 | Coherence Graph | 6 | 9 | 4 | 8 | 6.75 |

---

## 3. Base Selection

### Co-Bases: V2 (7.60) and V5 (7.55)

**Rationale for V2 as co-base**:

V2 scores highest overall due to its strong showing on implementation complexity (D3=8) and determinism (D4=9). The obligation scanner is the most implementation-ready code of any proposal, hooks cleanly into the existing MERGE_GATE via a single SemanticCheck, requires no pipeline model changes, and operates on the single merged roadmap (avoiding the multi-file access limitation that hampers V1, V4, and V5). Its unique detection axis -- scaffold-discharge pairing (U-003) -- catches a fundamentally different failure mode than omission-based approaches, making it a strong complement to V5.

**Rationale for V5 as co-base**:

V5 scores second overall and ties V2 on determinism (D4=9) while exceeding V2 on efficacy (D1=8 vs 7). The integration contract extractor is mechanism-aware (U-011) -- it does not just detect missing identifiers but verifies the roadmap contains explicit wiring tasks for specific integration mechanisms. The 7-category taxonomy (U-012) and extensible rule engine (U-013) provide a framework for ongoing expansion. V5's "mentioned is not planned" distinction (Round 2 debate) addresses a failure mode that simpler presence-checking solutions miss.

**Why V2+V5 as a pair**:

V2 and V5 address orthogonal failure modes with minimal duplication:
- V2 catches undischarged scaffolding (Phase 2 promises, Phase N does not fulfill)
- V5 catches missing integration wiring (spec defines dispatch table, roadmap does not plan to populate it)
- V2-A overlaps with V5-3 AP-001 only (diff analysis X-004), and the resolution is clean: V2-A's scanner algorithm becomes the implementation of V5-3's AP-001 rule
- Both are pure Python, zero LLM, and hook into existing gate infrastructure
- Combined implementation: ~450 LOC, 2 new files, 3 modified files

Both co-bases score D4=9 (fully deterministic), which is the critical property: the mitigation must not share the LLM blindspots that caused the original bug.

### Why not V4 (rank 3, score 6.90)?

V4 has the highest efficacy (D1=9) and the most innovative LLM-side technique (negative-space prompting), but its implementation complexity (D3=4) and semi-determinism (D4=6) drag down the composite. The hybrid requires 2 new files, 3 modified files, ~350 LOC, multi-file access workarounds, and an LLM pipeline step. Its strongest individual component (V4-2, fingerprint extraction) should be cherry-picked into the merge.

### Why not V1 (rank 4, score 6.75)?

V1's defense-in-depth is strategically sound but operationally heavy. The A+D+E combination spans deterministic and LLM layers, adding an LLM pipeline step that introduces the very non-determinism the proposal mitigates. V1's unique contribution -- the upstream guard (V1-C, spec structural audit) -- should be cherry-picked. The ID cross-reference (V1-A) is duplicated by V4-1 and partially covered by V4-2 fingerprints.

### Why not V3 (rank 5, score 6.75)?

V3 has the highest generalizability (D2=9) but the lowest efficacy (D1=6) and highest implementation complexity (D3=4). The coherence graph is the right long-term solution but the extraction heuristics are underspecified and carry the most implementation risk. V3's mapping to existing infrastructure (U-005) is valuable context for a later implementation phase. The graph should be a Phase 2 deliverable, not a Phase 1 base.

---

## 4. Cherry-Pick Recommendations

Elements from non-selected variants that complement the V2+V5 co-bases:

### Priority 1 (include in merge spec)

| Element | Source | What it adds | D-dimension gap it fills | Integration path |
|---------|--------|-------------|-------------------------|------------------|
| **Fingerprint extraction** | V4-2 | Mechanism-agnostic identifier coverage check | D1 (V2's D1=7 -> higher with fingerprints) | New module `fingerprint.py`, adds SemanticCheck to SPEC_FIDELITY_GATE. ~150 LOC. |
| **Spec structural audit** | V1-C | Upstream guard on extraction step quality | D2 (neither V2 nor V5 guard the extraction step) | New module `spec_structural_audit.py`, runs between extract and generate. ~80 LOC. |
| **Prompt constraint for integration enumeration** | V1-D + V5-2 merged | Prevention-layer reduces generation-time omissions | D1 (prevention reduces bug frequency before detection runs) | Modify `build_generate_prompt()` in prompts.py. ~50 lines of prompt text. |

### Priority 2 (defer to later phase)

| Element | Source | Why defer | When to add |
|---------|--------|----------|-------------|
| **Negative-space prompting** (with V1-E structured output) | V4-3 + V1-E | Adds LLM pipeline step cost; deterministic checks should be proven first | After V2+V5 deterministic checks ship and are validated in shadow mode |
| **Coherence graph** | V3-1 | Highest implementation risk; extraction heuristics need design work | Phase 2, after existing dataflow infrastructure is assessed for reuse |
| **Manifest + obligation ledger injection** | V3-2 + V2-B merged | Prevention layer; requires state management between pipeline steps | Phase 2, alongside coherence graph (shares extraction infrastructure) |

---

## 5. Merge Architecture Preview

The merged Anti-Instincts Gate combines V2 and V5 co-bases with V4-2 and V1-C cherry-picks:

```
Spec ──[V1-C: Structural audit]──> Extraction validated
                                         │
                                    [V1-D+V5-2: Prompt constraint]
                                         │
                              LLM generates roadmap
                                         │
                                    Merge step
                                         │
                          ┌──────────────┼──────────────┐
                          │              │              │
                    [V2-A: Obligation    [V5-1: Contract   [V4-2: Fingerprint
                     scanner]            extractor]         coverage]
                          │              │              │
                          └──────────────┼──────────────┘
                                         │
                              All checks pass?
                                         │
                                    ┌────┴────┐
                                    │ NO      │ YES
                                    │         │
                              GATE FAIL   Proceed to
                                         spec-fidelity
```

**Pipeline insertion**: Three deterministic checks run post-merge, before spec-fidelity. All are pure Python. Combined execution time: <1s.

**Gate definition**:

```python
ANTI_INSTINCT_GATE = GateCriteria(
    required_frontmatter_fields=[
        "undischarged_obligations",    # V2-A
        "uncovered_contracts",         # V5-1
        "fingerprint_coverage",        # V4-2
    ],
    enforcement_tier="STRICT",
    semantic_checks=[
        SemanticCheck(
            name="no_undischarged_obligations",
            check_fn=_no_undischarged_obligations,    # V2-A
            failure_message="Undischarged scaffolding obligations detected",
        ),
        SemanticCheck(
            name="integration_contracts_covered",
            check_fn=_integration_contracts_covered,  # V5-1 (executor workaround)
            failure_message="Spec integration contracts missing from roadmap",
        ),
        SemanticCheck(
            name="fingerprint_coverage_sufficient",
            check_fn=_fingerprint_coverage_check,     # V4-2
            failure_message="Spec code-level identifiers missing from roadmap",
        ),
    ],
)
```

**Files to create**:
- `src/superclaude/cli/roadmap/obligation_scanner.py` (V2-A, ~200 LOC)
- `src/superclaude/cli/roadmap/integration_contracts.py` (V5-1, ~250 LOC)
- `src/superclaude/cli/roadmap/fingerprint.py` (V4-2, ~150 LOC)
- `src/superclaude/cli/roadmap/spec_structural_audit.py` (V1-C, ~80 LOC)

**Files to modify**:
- `src/superclaude/cli/roadmap/gates.py` (add ANTI_INSTINCT_GATE + semantic checks)
- `src/superclaude/cli/roadmap/executor.py` (wire gate after merge, add structural audit after extract)
- `src/superclaude/cli/roadmap/prompts.py` (add integration enumeration block)

---

## 6. Convergence Assessment

Final convergence levels from Round 3:

| Key Decision | Convergence | Status |
|-------------|-------------|--------|
| V2+V5 as co-bases | 0.85 | ABOVE THRESHOLD (0.80) |
| V4-2 fingerprints as cherry-pick | 0.90 | ABOVE THRESHOLD |
| V1-C upstream guard as cherry-pick | 0.85 | ABOVE THRESHOLD |
| V3-1 deferred to Phase 2 | 0.80 | AT THRESHOLD |
| Deterministic checks = STRICT enforcement | 0.90 | ABOVE THRESHOLD |
| V4-3 negative-space deferred to Phase 2 | 0.75 | BELOW THRESHOLD (dissent from V4 advocate) |

**Dissent record**: V4-Advocate argues negative-space prompting should be Priority 1, not deferred. The existing spec-fidelity gate uses positive framing and failed; the adversarial reframing is needed now, not later. Counter-argument: three new deterministic checks (V2-A, V5-1, V4-2) provide sufficient detection depth without adding LLM cost. The negative-space prompt adds value but at a cost of one additional LLM call per pipeline run (~60s, ~$0.10). Defer until deterministic checks are validated.
