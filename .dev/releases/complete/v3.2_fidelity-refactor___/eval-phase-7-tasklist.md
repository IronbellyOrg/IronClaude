# Phase 7 — False-Positive Review and Threshold Hardening

Review ambiguous outcomes and tighten acceptance rules before claiming release proof.

---

### T07.01 — Review v3.1 ambiguity cases
**Roadmap Item IDs**: C1,X1,X2
**Tier**: STANDARD
**Effort**: M
**Steps**:
1. **[PLANNING]** Inspect any C1/X1/X2 outcomes marked ambiguous
2. **[EXECUTION]** Identify wording sensitivity, obligation vocabulary, or artifact insufficiency
3. **[VERIFICATION]** Decide whether to tighten fixture, verifier, or threshold
**Acceptance Criteria**:
1. Every ambiguous v3.1 result has an explicit disposition
2. Core-proof claims exclude unresolved ambiguity
**Validation**:
1. Review notes are saved under the eval root
**Dependencies**: T05.03

---

### T07.02 — Review v3.2 ambiguity cases
**Roadmap Item IDs**: C2,X1,X2,A1
**Tier**: STANDARD
**Effort**: M
**Steps**:
1. **[PLANNING]** Inspect zero-findings, whitelist, and provider-dir edge cases
2. **[EXECUTION]** Determine whether any result was falsely treated as clean
3. **[VERIFICATION]** Tighten verifier logic if needed
**Acceptance Criteria**:
1. Zero-findings outcomes have explicit justification
2. Blind-spot cases are separated from true passes
**Validation**:
1. Review notes and updated criteria are saved under the eval root
**Dependencies**: T06.02

---

### T07.03 — Review v3.05 ambiguity cases
**Roadmap Item IDs**: C3,A1
**Tier**: STANDARD
**Effort**: M
**Steps**:
1. **[PLANNING]** Inspect halt/progress interpretation edge cases
2. **[EXECUTION]** Verify whether budget behavior is directly evidenced or merely implied
3. **[VERIFICATION]** Tighten convergence acceptance rules if needed
**Acceptance Criteria**:
1. v3.05 proof claims are tied to persisted convergence evidence
2. Warning-only or indirect results are downgraded appropriately
**Validation**:
1. Review notes are saved under the eval root
**Dependencies**: T06.02
