---
total_diff_points: 12
shared_assumptions_count: 9
---

# Diff Analysis: Haiku-Analyzer vs Opus-Architect Roadmap Variants

## 1. Shared Assumptions and Agreements

1. **Phase 0 as blocking gate** — Both require empirical `--file` validation before code changes, with WORKING/BROKEN branching.
2. **PINEAPPLE sentinel test** — Identical validation approach for `--file` behavior.
3. **`--tools default` placement** — Both specify insertion between `--no-session-persistence` and `--max-turns` in `build_command()`.
4. **Kernel-derived constants** — Both define `_MAX_ARG_STRLEN`, `_PROMPT_TEMPLATE_OVERHEAD`, `_EMBED_SIZE_LIMIT` as module-level constants with assertion.
5. **Composed prompt guard** — Both measure `step.prompt + "\n\n" + embedded` with `<=` operator.
6. **Conditional Phase 1.5** — Both activate fallback remediation only if Phase 0 returns BROKEN, targeting the same four files.
7. **Test rename** — Both rename `test_100kb_guard_fallback` → `test_embed_size_guard_fallback`.
8. **Scope constraints** — Both explicitly defer stdin delivery, Windows 32 KB, prompt compression, and sprint orchestration redesign.
9. **UV-only execution** — Both mandate `uv run pytest` with no new imports in changed files.

---

## 2. Divergence Points

### D1 — Granularity of Timeline Estimates

| Aspect | Haiku-Analyzer | Opus-Architect |
|--------|---------------|----------------|
| Unit | Days (0.5–1.0 per phase) | Minutes/hours (15–60 min per phase) |
| Total WORKING | 3.5–4.0 days | 2–3 hours |
| Total BROKEN | 4.0–5.0 days | 3–4 hours |

**Impact**: Haiku's estimates suggest a multi-day effort with review cycles; Opus treats it as a focused half-day session. Opus is more realistic for the ~50 LOC production change described, but Haiku's padding may account for context-switching and review latency in a team setting.

### D2 — Phase Numbering and Parallelism Model

| Aspect | Haiku-Analyzer | Opus-Architect |
|--------|---------------|----------------|
| Structure | Phase 0 → 1 → 1.5 → 2 → 3 → 4 (strictly sequential) | Phase 0 → 1.1 ∥ 1.2 → 1.5 → 2 → 3 (parallel where possible) |
| FIX-001 and FIX-ARG parallelism | Sequential (Phase 1 then Phase 2) | Parallel (Phase 1.1 and 1.2 after Phase 0) |

**Impact**: Opus explicitly identifies that the two fixes are independent and can proceed in parallel after Phase 0, reducing wall-clock time. Haiku sequences them without justification for the dependency.

### D3 — Phase Organization Philosophy

| Aspect | Haiku-Analyzer | Opus-Architect |
|--------|---------------|----------------|
| Test phase | Phase 3 (after all implementation) | Phase 2 (immediately after implementation) |
| Validation phase | Phase 4 (separate from tests) | Phase 3 (combined integration validation) |

**Impact**: Haiku separates unit tests from integration validation into distinct phases. Opus collapses them more tightly. Haiku's separation provides clearer failure isolation; Opus's approach is more efficient for the small scope.

### D4 — Risk Probability Assessment for `--file` Fallback

| Aspect | Haiku-Analyzer | Opus-Architect |
|--------|---------------|----------------|
| `--file` broken probability | "Highest identified" (qualitative) | **80%** (quantitative) |

**Impact**: Opus commits to a specific probability estimate, which is more actionable for planning. Haiku hedges with qualitative language but provides stronger narrative justification for why this is the gating risk.

### D5 — Explicit Parallelism Notation in Risk Table

| Aspect | Haiku-Analyzer | Opus-Architect |
|--------|---------------|----------------|
| Format | Narrative prose per risk | Tabular with Prob/Impact/Phase columns |

**Impact**: Opus's table format is faster to scan and directly maps risks to phases. Haiku provides richer context per risk but requires more reading.

### D6 — Success Criteria Presentation

| Aspect | Haiku-Analyzer | Opus-Architect |
|--------|---------------|----------------|
| Format | Numbered list with requirement mappings | Validation matrix (SC-1 through SC-10) with test names and phases |

**Impact**: Opus's matrix is directly actionable — each criterion has a named test and phase. Haiku's list is correct but requires cross-referencing to determine how each criterion is verified.

### D7 — File Change Inventory

| Aspect | Haiku-Analyzer | Opus-Architect |
|--------|---------------|----------------|
| Explicit file list | Mentioned inline per phase | Dedicated table with change types |

**Impact**: Opus provides a clear worst-case file manifest. Haiku distributes this information across phases, making blast-radius assessment harder.

### D8 — Subclass Verification Approach

| Aspect | Haiku-Analyzer | Opus-Architect |
|--------|---------------|----------------|
| Approach | "Read subclass files before finalizing" (Phase 1) | Explicit step 1.1.1: "Read all subclasses to confirm no `super()` bypasses" |

**Impact**: Opus makes this a discrete, checkable step. Haiku mentions it as a guideline within the phase narrative.

### D9 — Performance Validation for `--tools default`

| Aspect | Haiku-Analyzer | Opus-Architect |
|--------|---------------|----------------|
| Approach | "Compare subprocess startup timing" in Phase 4 | Not explicitly called out as a validation step |

**Impact**: Minor. Haiku explicitly addresses NFR-001.1 with a timing comparison. Opus lists the risk (Risk 2) but doesn't specify a validation step for it.

### D10 — Executive Summary Framing

| Aspect | Haiku-Analyzer | Opus-Architect |
|--------|---------------|----------------|
| Framing | Risk-first narrative; leads with Phase 0 as gating decision | Delivery-first; leads with what ships, then describes the gate |

**Impact**: Haiku's framing is better for stakeholder communication when uncertainty is high. Opus's framing is better for implementers who want to know what to build.

### D11 — Open Questions Tracking

| Aspect | Haiku-Analyzer | Opus-Architect |
|--------|---------------|----------------|
| Format | Inline mentions throughout risk section | Dedicated "Open Questions for Post-Release" section |

**Impact**: Opus's dedicated section provides a clean handoff for the next release. Haiku embeds OQ references within risk narratives, requiring extraction.

### D12 — Scope Quantification

| Aspect | Haiku-Analyzer | Opus-Architect |
|--------|---------------|----------------|
| LOC estimate | Not provided | "~50 lines of production code, ~80 lines of test code" |

**Impact**: Opus's quantification helps calibrate effort and review expectations. Haiku omits this, which may contribute to its inflated timeline estimates.

---

## 3. Areas Where One Variant Is Clearly Stronger

### Opus-Architect is stronger in:
- **Actionability** — tabular formats, named test cases, file manifests, and LOC estimates make it immediately executable
- **Parallelism identification** — correctly identifies FIX-001 and FIX-ARG as independent, enabling parallel execution
- **Timeline realism** — estimates match the actual scope (~50 LOC production change)
- **Traceability** — SC-1 through SC-10 matrix with test names and phases

### Haiku-Analyzer is stronger in:
- **Risk narrative depth** — richer explanation of *why* each risk matters and what the residual concerns are
- **Phase 0 justification** — more compelling argument for why empirical validation must come first
- **Performance validation** — explicitly includes timing comparison for `--tools default` overhead
- **Defensive sequencing rationale** — explains why each phase ordering was chosen, not just what the order is

---

## 4. Areas Requiring Debate to Resolve

1. **Sequential vs parallel implementation of FIX-001 and FIX-ARG** — Opus says parallel; Haiku says sequential. The key question: does Phase 2's test suite need Phase 1's flag change to avoid false positives? If yes, Haiku is right about sequencing the implementation (but tests can still come after both). If no, Opus's parallelism is correct.

2. **Timeline calibration** — 3.5–5.0 days vs 2–4 hours is a 10x–20x disagreement. Need to clarify whether estimates include review cycles, context-switching, and stakeholder communication (Haiku's implicit assumption) or pure implementation time (Opus's assumption).

3. **Performance validation necessity** — Is a timing comparison for `--tools default` worth the effort, or is the risk low enough to skip? Haiku includes it; Opus doesn't.

4. **Test-implementation coupling** — Should tests land in the same phase as their corresponding fix (Opus) or in a dedicated test phase after all implementation (Haiku)? This affects failure diagnosis granularity vs development velocity.
