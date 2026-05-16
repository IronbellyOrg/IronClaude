# Base Selection

## Quantitative Scoring (50% weight)

| Metric | Weight | V1 (Architect) | V2 (Analyzer) | V3 (QA) |
|--------|--------|----------------|---------------|---------|
| Requirement Coverage (RC) | 0.30 | 0.92 | 0.85 | 0.95 |
| Internal Consistency (IC) | 0.25 | 0.95 | 0.85 | 0.92 |
| Specificity Ratio (SR) | 0.15 | 0.85 | 0.85 | 0.92 |
| Dependency Completeness (DC) | 0.15 | 1.00 | 1.00 | 1.00 |
| Section Coverage (SC) | 0.15 | 1.00 | 0.80 | 1.00 |
| **Quantitative subtotal** | | **0.941** | **0.865** | **0.953** |

Notes:
- RC: all variants cover all source phases. V3 preserves source phasing exactly; V1 adds Precondition 0; V2 folds 2+3.
- IC: V2 has mild internal tension between "iff cited" and "task-builder authoritative" framing (acknowledged in its critique §G-A2).
- SC: V2 is shorter (folded phase) and loses one major section's worth of structure relative to V1/V3.

## Qualitative Scoring (50% weight, 30 criteria additive binary)

### Dimension Subtotals

| Dimension (5 criteria) | V1 | V2 | V3 |
|------------------------|----|----|----|
| Completeness | 4 | 5 | 5 |
| Correctness | 5 | 4 | 5 |
| Structure | 5 | 5 | 5 |
| Clarity | 5 | 5 | 5 |
| Risk Coverage | 2 | 5 | 5 |
| Invariant & Edge Case Coverage | 5 | 1 | 5 |
| **Total** | **26 / 30** | **25 / 30** | **30 / 30** |
| qual_score | 0.867 | 0.833 | 1.000 |

### Per-Criterion Evidence (abbreviated CEV)

**Completeness**
- C1 covers all requirements: V1=MET, V2=MET, V3=MET
- C2 addresses edge cases: V1=MET (>10 proposal batching), V2=MET (Glob+absent), V3=MET (extensive)
- C3 includes deps/prereqs: all=MET
- C4 defines success criteria: V1=MET (register), V2=MET (G1-G5), V3=MET (G1-G8 + acceptance criteria)
- C5 specifies out of scope: V1=NOT MET (no excluded section in variant), V2=MET (deferred appendix), V3=MET (CASE-C deferred)

**Correctness**
- All MET except V2 — mild internal contradiction between "iff cited" and "authoritative" framing.

**Structure / Clarity** — all MET.

**Risk Coverage**
- V1 underperforms: only 2/5 (focuses structural, light on failure-mode and external-dependency risks).
- V2 and V3 both 5/5.

**Invariant & Edge Case Coverage**
- V1 = 5/5 — boundary cases (>10 proposals), state (register), guards (Precondition 0), count divergence (pass-batching), interaction (consults register).
- V2 = 1/5 — gate G1-G5 covers guard conditions; otherwise weak on boundaries, state-variable interactions, count-divergence, interaction effects. **Passes the 1/5 edge-case floor.**
- V3 = 5/5 — boundary (hard cap), state (state/ dir), guards (G1-G8), count divergence (cap), interaction (gates between phases).

## Edge Case Floor Check
- V1: 5/5 ≥ 1/5 — ELIGIBLE
- V2: 1/5 ≥ 1/5 — ELIGIBLE (at threshold)
- V3: 5/5 ≥ 1/5 — ELIGIBLE

All three variants eligible as base candidates.

## Position-Bias Mitigation

This compact run used a single qualitative pass per variant rather than dual-pass A→B→C / C→B→A. Documented as a protocol deviation (depth=quick mitigation). The +5% within-margin tiebreaker safeguard is not triggered (V3's margin exceeds 5% vs both V1 and V2).

## Combined Scoring

| Variant | Quant (×0.50) | Qual (×0.50) | Combined | Rank |
|---------|---------------|--------------|----------|------|
| V1 Architect | 0.471 | 0.434 | **0.904** | 2 |
| V2 Analyzer | 0.433 | 0.417 | **0.849** | 3 |
| V3 QA | 0.477 | 0.500 | **0.977** | 1 |

Margins:
- V3 vs V1: 0.977 − 0.904 = 0.073 (7.3%) — exceeds 5% tiebreaker margin; **no tiebreaker required**
- V3 vs V2: 0.977 − 0.849 = 0.128 (12.8%) — far exceeds margin
- V1 vs V2: 0.904 − 0.849 = 0.055 (5.5%) — exceeds margin

## Selected Base: Variant 3 — QA (quality-engineer, --persona-qa)

**Selection Rationale**

V3 leads on three of six qualitative dimensions (Completeness, Risk Coverage, Invariant/Edge Case Coverage), ties on the rest, and leads quantitatively as well. Its Global Failure-Mode Contract (G1-G7) provides the most comprehensive guard surface; its four-case conflict rule (CASE-A/B/C/D) covers gaps in the source's one-sided rule; its INPUT_SPEC routing fix prevents the prd skill from silently ignoring the release spec; its observable Acceptance Criteria section closes the source's aspirational test-plan gap; its convergence-below-threshold branch catches the highest-impact silent-pass failure mode (H-1 in V3's critique).

**Strengths to Preserve from V3 (Base)**
- Global Failure-Mode Contract G1-G7 (retry budgets, halt-or-degrade artifacts, decision gates, freshness, no invented flags, pipeline-log)
- Extended four-case conflict rule (CASE-A/B/C/D)
- Phase 4 explicit convergence-below-threshold branch
- Phase 7 five-step defense process for conflicting expert revisions + rejection-rate threshold
- Observable Acceptance Criteria propagating to PRD with mirror-check
- INPUT_SPEC routing fix (WHAT/WHERE append)
- 8-phase structure preserved (matches source)
- /sc:reflect retained per user's explicit request to engage it

**Strengths to Incorporate from V1 (Architect)**
- `conflict-register.md` as a single append-only precedence ledger (V1's U-001). The four-case rule benefits from a file-mediated audit trail; the register makes case decisions visible across phases without requiring downstream phases to re-derive them from state/ files.
- Explicit Phase 3 Step 3.4 — `proposals/INDEX.md` manifest containing the literal comma-separated path list for `--compare`. Removes ambiguity at Phase 4 invocation time.
- Phase 7 `--downstream roadmap` REMOVAL with documented rationale. spec-panel.md Step 6b activates roadmap-oriented frontmatter that the prd skill (the actual downstream consumer) ignores.
- Phase 8 `SUPPORTING_INPUTS` to prd skill (conflict-register + merge-log + reflect output). Routes additional context the PRD can trace decisions through.
- Phase 1 Step 1.0 explicit subdirectory pre-creation (touch + Read for hook compliance before any phase writes).

**Strengths to Incorporate from V2 (Analyzer)**
- Outcome-bounded Sequential thought count (replace "15-25 minimum" with "stop when each row has source-grounded justification"). V2's critique §A-001 has clear evidence.
- `/sc:adversarial --depth standard` with conditional escalation to `deep` only when a proposal's cited risk is HIGH. FINAL-REPORT §6.1 ran the prior study at depth=quick and converged at 0.81 mean. (Source's `deep` is cargo-cult per V2 §A-003.)
- Drop `/sc:adversarial --interactive`. Batch-replayable orchestration contract is cleaner; the source's `--interactive` introduces an undocumented human-in-loop requirement that Phases 5-8 don't know about. (V2 §A-011.)
- Required proposal-header fields `final_report_citation` and `direction_inversion_basis` enforced as halt conditions (V2 §A-004). Closes the inversion-symmetry evidence gap (V2 §G-A1).
- Glob-and-report-absent rule for Bucket D (rf-* agents) and Bucket F (sample release specs) — V2 verified Bucket F is empty in this repo at orchestration time (V2 §A-007).

**Strengths Rejected (kept from base, not incorporated)**
- V2's Phase 2+3 folding into single `analysis.md`. Rejected: collapses the audit trail; V1's critique §W4 and V3's preserved structure both prefer separation. Keep V3's two-phase structure.
- V2's outright replacement of `/sc:reflect` with the Citation Gate. The user explicitly asked for `/sc:reflect` engagement throughout the orchestration; replacement overshoots. INCORPORATE V2's gate as an ADDITIONAL artifact (`gate-report.md`) inside Phase 5, rather than substituting for /sc:reflect. Reflect runs first; gate validates its output.
- V2's drop of `--convergence 0.80`. Rejected: V3's explicit 0.80 + sub-threshold branch (Phase 4) is the stronger contract; the protocol default value is not verified in this repo, so omitting risks a weaker bar.
- V3's retention of `--downstream roadmap`. Rejected per V1's evidence-backed flag-removal argument.
- V3's sequential single-value `--focus` passes (Phase 4). The /sc:adversarial command file's examples use comma-list focus values (`--focus structure,completeness`) at adversarial.md:97. Restore comma-list usage; document this as V3-deviation in merge-log.
