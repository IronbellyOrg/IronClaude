# Validation Report Scoring Matrix

## Head-to-Head Comparison

| Dimension | Variant A (Claude) | Variant B (GPT) | Winner |
|-----------|-------------------|-----------------|--------|
| **Accuracy** | 72/100 | 85/100 | **Variant B** |
| **Completeness** | 80/100 | 68/100 | **Variant A** |
| **False Positive Rate** | 4.8% (4/84 rejected) | 0% (0 rejected) | **Variant A** (lower is better — A tracked and removed FPs) |
| **False Negative Rate** | 9.5% (2 missed conflicts) | 1.5% (1 missed NSD) | **Variant B** |
| **Contradictions Found** | 7 points of disagreement identified | — | See detail below |

---

## Dimension Detail

### 1. Accuracy (0-100)

**Variant A: 72/100**
- D1 domain score (100%) is provably wrong — adversarial pass contradicts it
- Requirement count (84) inflated by ~30% over ground truth (65)
- Coverage scores (93.5% weighted) are artificially high due to inflated denominator
- All 4 MISSING FRs correctly identified (via adversarial pass)
- Integration wiring over-optimistic (FULLY_WIRED where PARTIALLY_WIRED is correct)
- FR-7.1/7.3 conflicts completely missed

**Variant B: 85/100**
- Requirement count (62) within 5% of ground truth (65) — most accurate
- Coverage scores (84.7%) closely match recalculated ground truth (84.6%)
- All 4 MISSING FRs correctly identified in primary pass (not needing adversarial)
- FR-7.1 schema conflict correctly caught
- FR-7.3 flush semantics correctly caught
- FR-5.2 positive-case gap correctly caught
- Minor: GAP-H007 severity potentially overstated (MEDIUM more appropriate than HIGH)
- Minor: missed NSD-001 spec ambiguity

### 2. Completeness (0-100)

**Variant A: 80/100**
- 7 domain agents + 4 cross-cutting agents = wider coverage surface
- 84 requirements tracked (overcounted, but attempted comprehensive decomposition)
- Explicit adversarial pass with [ADV] tagging
- REJECTED findings section documents false-positive adjudication
- NEEDS-SPEC-DECISION escalation for genuine ambiguities
- 11 agent report files
- **Missing**: FR-7.1 schema conflict, FR-7.3 flush conflict, FR-5.2 positive-case, FR-6.1/6.2 specificity

**Variant B: 68/100**
- 4 domains + 4 cross-cutting agents = narrower coverage surface
- 62 requirements tracked (slightly under-counted)
- No explicit adversarial pass separation
- No REJECTED findings section
- No NEEDS-SPEC-DECISION section
- 8 agent report files
- **Found that A missed**: FR-7.1 schema, FR-7.3 flush, FR-5.2 positive-case, FR-6.1/6.2 specificity, count inconsistency

### 3. False Positive Rate

**Variant A: 4.8%** (4 CC4 findings correctly rejected out of ~84 evaluated items)
- C1: handle_regression → REJECTED (FR-2.1a covers it)
- C2: SHADOW_GRACE_INFINITE → REJECTED (FR-1.19 covers it)
- C3: __post_init__() → REJECTED (FR-1.20 covers it)
- H5: check_wiring_report() → REJECTED (FR-1.21 covers it)
- All rejections are correct — the spec DOES have these FRs; the ROADMAP is what's missing them

**Variant B: Unmeasured** (0 rejected findings reported)
- This does NOT mean 0 false positives — it means false-positive tracking was not performed
- All 15 findings in Variant B are substantively valid upon ground-truth check
- However, GAP-H007 severity is arguable (HIGH vs MEDIUM for a presentational issue)

### 4. False Negative Rate

**Variant A: 9.5%** — missed 2 genuine HIGH-severity findings that exist in the spec-roadmap delta:
1. FR-7.1 `duration_ms` schema omission (verified: roadmap L47 lists 9 fields, spec shows 10)
2. FR-7.3 flush semantics conflict (verified: "session end" vs "after each test")
- Also missed: FR-5.2 positive-case gap (MEDIUM)

**Variant B: 1.5%** — missed 1 genuine finding:
1. NSD-001 spec ambiguity (FR-7.1 vs FR-7.3 `assertion_type`) — LOW impact

### 5. Contradictions Between Reports

| # | Requirement | Variant A Verdict | Variant B Verdict | Ground Truth |
|---|------------|------------------|------------------|--------------|
| 1 | FR-1.19 (SHADOW_GRACE_INFINITE) | COVERED (D1) then MISSING (ADV) | MISSING (H001) | **MISSING** — both ultimately correct; B caught it faster |
| 2 | FR-1.20 (__post_init__) | COVERED (D1) then MISSING (ADV) | MISSING (H002) | **MISSING** — same pattern |
| 3 | FR-1.21 (check_wiring_report) | COVERED (D1) then MISSING (ADV) | MISSING (H003) | **MISSING** — same pattern |
| 4 | FR-2.1a (handle_regression) | COVERED (D2) then MISSING (ADV) | MISSING (H004) | **MISSING** — same pattern |
| 5 | FR-7.1 (audit schema fields) | Not flagged | CONFLICTING (H005) | **CONFLICTING** — Variant B correct |
| 6 | FR-7.3 (flush semantics) | Not flagged | CONFLICTING (H006) | **CONFLICTING** — Variant B correct |
| 7 | FR-5.2 (positive-case test) | Not flagged | PARTIAL (M002) | **PARTIAL** — Variant B correct |

---

## Overall Winner Determination

| Criterion | Weight | Winner | Margin |
|-----------|--------|--------|--------|
| Accuracy | 30% | **Variant B** | +13 points (85 vs 72) |
| Completeness | 25% | **Variant A** | +12 points (80 vs 68) |
| False Positive Rate | 15% | **Variant A** | A tracks FPs; B doesn't measure |
| False Negative Rate | 20% | **Variant B** | 1.5% vs 9.5% — dramatically better |
| Process Rigor | 10% | **Variant A** | 7-domain, [ADV] tagging, REJECTED section |

**Weighted Score**:
- Variant A: (72×0.30) + (80×0.25) + (85×0.15) + (50×0.20) + (90×0.10) = 21.6 + 20.0 + 12.75 + 10.0 + 9.0 = **73.35**
- Variant B: (85×0.30) + (68×0.25) + (60×0.15) + (95×0.20) + (65×0.10) = 25.5 + 17.0 + 9.0 + 19.0 + 6.5 = **77.00**

### **Winner: Variant B (GPT) — 77.0 vs 73.4**

Variant B wins primarily on **accuracy** (closer requirement count, no internal contradictions, correct coverage scores) and **false negative rate** (caught FR-7.1/7.3 conflicts that Variant A missed entirely). These are the two most impactful dimensions for a validation report — its core job is to find what's wrong.

Variant A wins on **completeness** (wider agent coverage, more systematic process) and **process rigor** (REJECTED section, [ADV] tagging, NEEDS-SPEC-DECISION). These are valuable for report credibility but secondary to finding actual gaps.

### **Best outcome: The adversarial merge** combines Variant A's structural rigor with Variant B's superior finding accuracy. The merged report at `validation-comparison/merged-consolidated-report.md` incorporates all valid findings from both reports with ground-truth-verified metrics.
