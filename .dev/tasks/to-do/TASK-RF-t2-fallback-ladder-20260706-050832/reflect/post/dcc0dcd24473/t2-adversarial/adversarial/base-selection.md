# Base Selection

## Quantitative Scoring (50% weight)

| Metric | Weight | V1 (qwen) | V2 (glm) | Notes |
|--------|--------|-----------|----------|-------|
| Requirement coverage (RC) | 0.30 | 0.90 | 0.70 | V1 covers verdict-honesty, additive-only, proxy-safety, test-coverage, process; V2 truncated before its Pass/Fail synthesis |
| Internal consistency (IC) | 0.25 | 0.85 | 0.90 | V1 carries one false-positive (#3); V2 internally consistent but incomplete |
| Specificity ratio (SR) | 0.15 | 0.80 | 0.90 | V2 gives per-finding file:line + frontmatter field cites |
| Dependency completeness (DC) | 0.15 | 0.90 | 0.60 | V2 truncation leaves M2 dangling; no closing synthesis |
| Section coverage (SC) | 0.15 | 1.00 | 0.55 | V1 = 5 sections (findings/suspect-table/signals/recs); V2 truncated |
| **quant_score** | | **0.882** | **0.751** | |

## Qualitative Scoring (50% weight) — Additive Binary Rubric (30 criteria)

| Dimension (5 each) | V1 met | V2 met | Decisive evidence |
|--------------------|--------|--------|-------------------|
| Completeness | 5 | 2 | V2 truncated mid-M2; no verdict synthesis, no signal table, no recommendations |
| Correctness | 3 | 4 | V1 #3 is a ground-truth false positive; V2's H2 CONFIRMED, H1 real (H4 over-stated) |
| Structure | 5 | 3 | V1 full section scaffold; V2 incomplete |
| Clarity | 4 | 5 | V2 file:line + explicit scorer actions per finding |
| Risk Coverage | 4 | 4 | V1 suspect-source risk table; V2 gate-integrity risk (H2) |
| Invariant & Edge-Case (L3) | 2 | 4 | V2 probes gate *mechanics* (H1 label-class, H2 anti-bias substitution — state-mechanics level); V1 mostly L2 process |
| **qual_score** (/30) | **23/30 = 0.767** | **22/30 = 0.733** | |

**Edge-case floor (1/5):** V1 = 2/5, V2 = 4/5 → both eligible as base.

## Position-Bias Mitigation
- Pass 1 (V1, V2) and Pass 2 (V2, V1) evaluated; the only criterion that flipped was **Correctness** — reverse-order surfaced that V2's confirmed H2 should outweigh V1's cleaner-but-shallower correctness. Re-evaluation upheld V2 Correctness = 4, V1 = 3. All other criteria agreed across passes.

## Combined Scoring

| Variant | quant×0.50 | qual×0.50 | **Combined** |
|---------|-----------|-----------|--------------|
| **V1 (qwen)** | 0.441 | 0.384 | **0.825** |
| **V2 (glm)** | 0.376 | 0.367 | **0.742** |

Margin = 0.083 (8.3%) → **above the 5% tiebreaker band**; no tiebreaker needed.

## Selected Base: Variant 1 (qwen3.6-plus)

**Selection rationale.** V1 wins the combined score decisively — driven by completeness (V2 is truncated mid-sentence and cannot serve as a structural base) and section coverage. A base must be a *complete* artifact into which strengths are grafted; a truncated review disqualifies itself as the scaffold even though it carries the higher-value individual findings.

**Strengths to preserve (from V1 base):**
- The full section scaffold: Concrete Findings → Suspect-Source risk table → Pass/Fail Signals → Recommendations.
- The additive-only 0-diff confirmation (`contract.py` + `swarm/models.py` byte-unchanged) — the correct headline.
- Unique catch **#5** (eager→lazy `_lazy_openai_factory` design drift).
- The suspect-source file risk routing table.

**Strengths to incorporate (from V2 non-base):**
- **H2** (6.G11 spawned-verification substitution) — CONFIRMED; promote to the top IMPORTANT finding. **V1 entirely lacks this.**
- **H1** (carve-out label vs rationale) — add as IMPORTANT with the recalibrated "document-don't-reverse" disposition.
- **H3** framing — replace V1's "Security/Process" tag on the HALT finding with V2's auditability framing (project norm: no security framing).
- V2's per-finding **file:line** citation discipline.

**Corrections mandated by ground truth (applied during merge):**
- **DROP** V1 #3 "Metadata Drift" (head==start_commit is working-tree-diff by design — frontmatter L46).
- **DOWNGRADE** V1 #1 (untracked test) IMPORTANT → MINOR (file exists, green, documented over-delivery).
- **DOWNGRADE** V2 H1 CRITICAL → IMPORTANT; V2 H4 HIGH → LOW (dispositioned at `final-fulltest-summary.md:23`).
- **RECONCILE** verdict → **CONDITIONAL PASS with mandatory documented follow-ups** (not V2's FAIL: the load-bearing guarantee holds and the suite is green; not V1's unqualified PASS: H1/H2 are real and must be dispositioned).
