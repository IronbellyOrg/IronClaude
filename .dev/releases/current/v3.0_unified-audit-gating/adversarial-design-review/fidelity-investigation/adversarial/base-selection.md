# Base Selection & Consolidated Findings

## Metadata
- Generated: 2026-03-19
- Analysis type: Fidelity gate convergence investigation
- Scoring focus: Effectiveness at mitigating 5 empirical root causes

---

## 1. Consolidated Findings Table (Spec × Root-Cause Matrix)

### Scoring: 1-5 Scale
1 = no mitigation, 2 = weak, 3 = partial, 4 = strong, 5 = complete

#### For Each Spec's OWN Gate

| Root Cause | Spec A (Wiring v2.0) | Spec B (Anti-Instincts) | Spec C (Wiring v1.0) |
|------------|---------------------|------------------------|---------------------|
| RC1: Severity Drift | **5** — Code-enforced Literal enum | **5** — Binary pass/fail, no gradient | **5** — Zero-tolerance, all counts=0 |
| RC2: Document Regeneration | **5** — retry_limit=0, Python emitter | **5** — retry_limit=0, Python emitter | **4** — Sprint-only, no roadmap step |
| RC3: Attention Degradation | **5** — AST analysis, no LLM | **5** — Regex/counting, no LLM | **5** — AST analysis, no LLM |
| RC4: Goalpost Movement | **5** — Mode-aware blocking_for_mode() | **5** — Fixed thresholds (0.7, 0, 0) | **5** — All-zero-tolerance |
| RC5: No Convergence | **5** — Avoids via retry_limit=0 | **5** — Avoids via retry_limit=0 | **4** — Sprint focus, no pipeline retry |
| **Own-Gate Total** | **25/25** | **25/25** | **23/25** |

#### For the EXISTING Spec-Fidelity Gate (the actual broken component)

| Root Cause | Spec A (Wiring v2.0) | Spec B (Anti-Instincts) | Spec C (Wiring v1.0) |
|------------|---------------------|------------------------|---------------------|
| RC1: Severity Drift | **1** — Does not touch fidelity gate | **1** — Does not touch fidelity gate | **2** — Deviation recon catches count inconsistency |
| RC2: Document Regeneration | **1** — Does not address remediation | **2** — Prompt injection improves generation quality | **1** — Does not address roadmap pipeline |
| RC3: Attention Degradation | **1** — Does not reduce fidelity prompt burden | **0** — WORSENS: adds 6th comparison dimension | **1** — Does not address fidelity prompt |
| RC4: Goalpost Movement | **1** — Severity definitions don't apply to fidelity | **1** — Binary thresholds don't apply to fidelity | **2** — Deviation recon partially anchors counts |
| RC5: No Convergence | **1** — No memory mechanism for fidelity gate | **1** — No memory mechanism for fidelity gate | **1** — No memory mechanism for fidelity gate |
| **Fidelity-Gate Total** | **5/25** | **5/25** (net: 4/25 after RC3 penalty) | **7/25** |

---

## 2. Gap Analysis: Root Causes with NO Mitigation Across All 3 Specs

### CRITICAL GAPS

| Root Cause | Gap Status | Evidence |
|------------|-----------|----------|
| **RC1: Severity Drift** | ⚠️ MINIMAL — Only C's deviation recon touches this, and only for count consistency, not severity judgment anchoring | No spec defines a canonical severity rubric for the spec-fidelity gate's LLM |
| **RC2: Document Regeneration** | ⚠️ MINIMAL — B's prompt injection helps at generation time but not at remediation time | No spec constrains the remediation step to preserve structure |
| **RC3: Attention Degradation** | 🔴 **ZERO MITIGATION** — No spec reduces the spec-fidelity prompt's token burden. B actively worsens it. | All specs embed full documents inline; B adds a 6th dimension |
| **RC4: Goalpost Movement** | ⚠️ MINIMAL — C's deviation recon catches count inconsistency but doesn't anchor severity definitions | No spec provides a canonical "what is HIGH" definition for fidelity deviations |
| **RC5: No Convergence Mechanism** | 🔴 **ZERO MITIGATION** — No spec adds memory, prior-run context, or convergence tracking to the fidelity gate | All 3 specs avoid convergence in their own gates but ignore the existing gate |

### Summary

- **2 root causes have ZERO mitigation across all 3 specs**: RC3 (Attention Degradation) and RC5 (No Convergence Mechanism)
- **3 root causes have MINIMAL mitigation**: RC1, RC2, RC4 — each has at most a weak indirect touch from one spec
- **All 5 root causes are fully mitigated for the NEW gates** being introduced, but NONE are adequately addressed for the EXISTING broken gate

---

## 3. Effectiveness Ranking

### Ranking for Addressing the Infinite Loop Problem

| Rank | Spec | Fidelity-Gate Score | Rationale |
|------|------|--------------------:|-----------|
| **1** | **Spec C (Wiring v1.0)** | 7/25 | Only spec that directly modifies SPEC_FIDELITY_GATE (deviation count reconciliation). Narrow but real. |
| **2** | **Spec A (Wiring v2.0)** | 5/25 | Most comprehensive architectural design, but does not touch the broken gate. Its pattern (retry_limit=0, deterministic) is the correct *model* for a fix. |
| **3** | **Spec B (Anti-Instincts)** | 4/25 (net) | Prompt injection helps generation quality but adds attention burden to the fidelity check. Net negative on RC3. |

### Ranking for Overall Gate Quality

| Rank | Spec | Own-Gate Score | Rationale |
|------|------|---------------:|-----------|
| **1** | **Spec A (Wiring v2.0)** | 25/25 | Most detailed, mode-aware, dual-mode operation, explicit retry_limit=0 semantics |
| **2** | **Spec B (Anti-Instincts)** | 25/25 | Unified 4-module defense, prompt-level prevention, binary pass/fail simplicity |
| **3** | **Spec C (Wiring v1.0)** | 23/25 | Solid foundation but sprint-only scope, no roadmap pipeline integration |

---

## 4. Concrete Recommendations for a Refactored Fidelity System

Based on this analysis, the spec-fidelity gate needs a dedicated refactoring release that addresses the 5 root causes directly. The 3 analyzed specs provide excellent *patterns* (deterministic Python, retry_limit=0, code-enforced severity) but none directly fix the broken component.

### Recommendation 1: SEVERITY ANCHORING (fixes RC1 + RC4)

**Problem**: Each LLM invocation independently interprets what "HIGH severity" means.

**Fix**: Create a canonical severity rubric as a structured data artifact, not prompt prose.

```python
# Proposed: fidelity_severity_rubric.py
SEVERITY_RUBRIC = {
    "HIGH": {
        "definition": "Spec requirement is absent from roadmap OR roadmap contradicts spec",
        "examples": [
            "Spec defines FR-001 but roadmap has no corresponding task",
            "Spec requires X; roadmap plans NOT-X",
        ],
        "test": lambda spec_req, roadmap_text: spec_req.id not in roadmap_text,
    },
    "MEDIUM": {
        "definition": "Spec requirement is partially addressed — present but incomplete",
        "examples": [
            "Spec defines 5 acceptance criteria; roadmap addresses 3",
            "Spec requires integration test; roadmap has only unit test",
        ],
    },
    "LOW": {
        "definition": "Cosmetic or organizational deviation — no functional impact",
        "examples": [
            "Different section ordering than spec suggests",
            "Different naming convention than spec uses",
        ],
    },
}
```

**Pattern source**: Variant A's `WiringFinding.severity` Literal enum with code-level definitions.

### Recommendation 2: DETERMINISTIC PRE-FILTER (fixes RC3 partially)

**Problem**: The fidelity check prompt embeds full spec + full roadmap, causing attention drift.

**Fix**: Run deterministic pre-checks (fingerprint coverage, integration contracts, obligation scanning) BEFORE the LLM fidelity check. Only send UNSATISFIED items to the LLM for severity assessment.

```
Phase 1 (deterministic): Extract requirements, check presence → produces "mechanically verified" set
Phase 2 (LLM, reduced scope): Only assess severity for items NOT mechanically verified
```

**Pattern source**: Variant B's 4-module approach (obligation scanner + contract extractor + fingerprint + structural audit) — use these as the deterministic pre-filter.

**Benefit**: Reduces the LLM's task from "find all deviations in 2 huge documents" to "assess severity of these 5 specific items." Dramatically reduces attention burden.

### Recommendation 3: REMEDIATION MEMORY (fixes RC5)

**Problem**: Each remediation run starts from zero context about prior findings.

**Fix**: Persist a `fidelity-findings-ledger.yaml` that records all findings from all runs with their severity, and pass it to subsequent runs as anchoring context.

```yaml
# fidelity-findings-ledger.yaml (persisted between runs)
run_1:
  timestamp: 2026-03-19T10:00:00
  findings:
    - id: DEV-001
      severity: HIGH
      description: "FR-001 absent from roadmap"
      status: open
run_2:
  timestamp: 2026-03-19T10:05:00
  findings:
    - id: DEV-001
      severity: HIGH  # ANCHORED to run_1's severity
      description: "FR-001 absent from roadmap"
      status: fixed  # remediation addressed it
    - id: DEV-002
      severity: MEDIUM
      description: "FR-003 partially addressed"
      status: open
```

**Convergence rule**: A finding's severity CANNOT change between runs unless the underlying content changed. If DEV-001 was HIGH in run 1, it's HIGH in run 2 unless the roadmap text for that requirement changed.

**Pattern source**: Variant A's `retry_limit=0` avoids convergence, but for the fidelity gate (which MUST use LLM judgment), we need explicit convergence — the ledger provides it.

### Recommendation 4: STRUCTURE-PRESERVING REMEDIATION (fixes RC2)

**Problem**: The LLM sometimes regenerates the entire roadmap rather than making targeted edits.

**Fix**: The remediation prompt should receive the roadmap as a diff target, not a generation target. Instead of "here's the spec and the fidelity report, produce a fixed roadmap," the prompt should be "here are 3 specific findings to fix in the existing roadmap — modify ONLY the sections listed."

```python
# Proposed remediation prompt structure
REMEDIATION_PROMPT = """
You are editing an existing roadmap. DO NOT regenerate the full document.

EXISTING ROADMAP (preserve all content not listed in fixes):
{roadmap_content}

FIXES TO APPLY (modify ONLY these sections):
{for each open finding in ledger:}
  - Finding {id}: {description}
    Location in roadmap: {section_ref}
    Required change: {specific_fix_instruction}

Output the FULL roadmap with ONLY the listed fixes applied.
All other content must be IDENTICAL to the input.
"""
```

**Pattern source**: Variant A's `emit_report()` (Python writes the report, ensuring structural stability) — apply the same principle to remediation by constraining the LLM to targeted edits.

### Recommendation 5: CONVERGENCE CEILING (fixes RC5 + RC1)

**Problem**: After 4 runs, the gate cannot converge to 0 HIGH deviations.

**Fix**: Set a hard convergence ceiling: maximum 3 remediation attempts. After 3 attempts, the gate switches to a "manual review required" state rather than looping infinitely.

```python
MAX_REMEDIATION_ATTEMPTS = 3

# In the remediation loop:
if attempt >= MAX_REMEDIATION_ATTEMPTS:
    logger.warning(
        f"Fidelity gate: {high_count} HIGH deviations after "
        f"{MAX_REMEDIATION_ATTEMPTS} attempts. Manual review required."
    )
    # Write remediation report with remaining findings
    # Set gate to TRAILING mode (log but don't block)
    return GateResult(status="manual_review", findings=remaining)
```

**Pattern source**: Variant A's `retry_limit=0` is the extreme form of this (0 retries). For the fidelity gate, 0 retries isn't viable (LLM output needs iteration), but a hard ceiling prevents infinite loops.

---

## 5. Recommended Priority Order

| Priority | Recommendation | Root Causes Fixed | Effort |
|----------|---------------|-------------------|--------|
| **P0** | R5: Convergence ceiling (max 3 attempts) | RC5 | ~20 LOC |
| **P0** | R3: Remediation memory (findings ledger) | RC5, RC1 | ~80 LOC |
| **P1** | R4: Structure-preserving remediation prompt | RC2 | ~40 LOC (prompt change) |
| **P1** | R1: Severity anchoring rubric | RC1, RC4 | ~60 LOC |
| **P2** | R2: Deterministic pre-filter | RC3 | ~200 LOC (leverages B's modules) |

**Total estimated effort**: ~400 LOC — comparable to a single one of the analyzed specs.

**Key insight**: The cheapest fix (R5, ~20 LOC) immediately breaks the infinite loop. The most impactful fix (R3, ~80 LOC) prevents severity drift. These two together would have prevented the problem that triggered this investigation.
