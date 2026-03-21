---
pipeline: adversarial-5-agent-debate
source_spec: wiring-verification-gate-v1.0-release-spec.md
date: 2026-03-17
agents: 5
recommendations_debated: BC-1, BC-2, BC-3, NB-1, NB-2
---

# Adversarial Debate Synthesis — Wiring Verification Gate v1.0

## Per-Recommendation Verdicts

### BC-1: Callable Annotation Normalization Algorithm

| Dimension | Score |
|-----------|-------|
| Validity | PARTIALLY valid |
| Blocking classification | SHOULD BE ADVISORY |
| Confidence | High (Agent found codebase evidence) |

**Key findings:**
- `ast.unparse()` canonicalization step is **genuinely missing** from the spec and must be added — without it, the algorithm is not directly implementable
- Word-boundary regex (`\bCallable\b`) is a **legitimate improvement** over substring search — prevents false positives on names like `CallableWidget` or `NotCallableType`
- The PEP 563 / `eval()` recommendation is **technically incorrect** — `ast.parse()` always returns AST nodes regardless of `from __future__ import annotations`; the concern about manually-quoted forward references is real but handled correctly by `ast.unparse()` without `eval()`
- SC-010 is **not at risk** — the actual `cli_portify` annotation uses `Optional[Callable[...]]` which `ast.unparse()` handles correctly

**Debate outcome**: Adopt the spec improvement (normalization + regex), drop the `eval()`/PEP 563 note, reclassify from BLOCKING to advisory (spec improvement before T02 is still warranted). The proposed spec text from Agent 1 is technically superior to the panel's original recommendation.

---

### BC-2: YAML Frontmatter Injection Prevention

| Dimension | Score |
|-----------|-------|
| Validity | PARTIALLY valid |
| Blocking classification | SHOULD BE ADVISORY |
| Confidence | Medium |

**Key findings:**
- The `yaml.safe_dump()` recommendation is **correct as engineering practice** — f-string interpolation of paths into YAML is structurally defective
- The threat model is **overstated** for this gate — the gate-critical fields evaluated by `SemanticCheck` (`analysis_complete`, `unwired_count`) are booleans and integers derived from computation, not from injectable string inputs
- The realistic risk is **malformed YAML in metadata fields** (e.g., `target_dir` with a colon) causing a report parse error, which defensively handled produces a safe failure, not a silent bypass
- TC-16 has **independent regression value** regardless of threat model classification

**Debate outcome**: Adopt `yaml.safe_dump()` for string-valued metadata fields and TC-16, reclassify from BLOCKING to advisory (required before production stabilization, not before T05). The spec text should distinguish between gate-evaluated fields (exempt) and metadata fields (require `yaml.safe_dump()`).

---

### BC-3: Explicit Test Matrix and SC-010 Fixture Specification

| Dimension | Score |
|-----------|-------|
| Validity | PARTIALLY valid |
| Blocking classification | SPLIT — coverage requirements BLOCK T06, fixture source code does NOT |
| Confidence | High |

**Key findings:**
- "11 unit tests" is **not a coverage specification** — it is a headcount; the behavioral coverage requirements must be in the spec
- TC-04 (alias) and TC-05 (kwargs) **conflict with the spec's stated scope** — dynamic dispatch is explicitly excluded; these TCs would either expand scope or test vacuously
- TC-09 (neg-`__init__.py`-reexport) and TC-10 (private), TC-11 (conftest) are **genuinely necessary** negative cases that will be missed without explicit enumeration
- The SC-010 fixture source code (class names, file names, parameter names) **belongs at T06 implementation time**, not in the release spec; only the behavioral contract belongs in the spec
- The 18-test matrix should be reduced to **16 tests** (remove TC-04 and TC-05), separated into unit (14) and integration (2) layers

**Debate outcome**: Replace Section 9 with behavioral coverage requirements (not numbered TCs), specify SC-010 as a behavioral contract (not source code), remove TC-04/TC-05 as out-of-scope. Blocking condition survives but is narrowed to "Section 9 must specify coverage categories" before T06.

---

### NB-1: Import Re-export False Positive Risk and Convention Mismatch

| Dimension | Score |
|-----------|-------|
| Validity | PARTIALLY valid |
| Blocking classification | NON-BLOCKING for v1.0; split on which parts belong in v1.0 vs v1.1 |
| Confidence | High |

**Key findings:**
- The re-export blind spot **will produce systematic false positives** in Phase 1 shadow mode — this is a real algorithmic limitation
- However, the **3-hop import alias pre-pass is v1.1 work**, not v1.0 work — the complexity (star imports, `__all__`, conditional imports, `TYPE_CHECKING`) is significant and shadow mode is explicitly designed to tolerate FPR
- The **correct v1.0 response** is: document the limitation in Section 4.2.1, add an FPR range guidance table to Section 8, adjust Phase 2 thresholds accordingly
- W1.3 (convention mismatch: default `provider_dir_names` won't match this codebase) is the **more severe defect** — it produces a silent null result on first run, indistinguishable from a clean codebase
- The minimal fix for W1.3 is: mandatory pre-activation validation checklist in Section 8 + zero-findings sanity check

**Debate outcome**: Do NOT add the import alias pre-pass to v1.0 spec. DO add: (1) known limitation note to Section 4.2.1, (2) FPR range table to Section 8, (3) pre-activation checklist with provider_dir validation and zero-findings sanity check, (4) threshold calibration guidance for Phase 2.

---

### NB-2: Whitelist Audit Schema and Controls

| Dimension | Score |
|-----------|-------|
| Validity | PARTIALLY valid |
| Blocking classification | NON-BLOCKING; tiered by phase |
| Confidence | High |

**Key findings:**
- `whitelist_entries_applied: N` in frontmatter is **high-value, zero-cost** — must go in v1.0
- Schema validation (required `symbol`, non-empty `reason`) is **reliability engineering**, not security theater — must go in v1.0
- `WiringConfigError` hard failure on malformed whitelist should be **Phase 2** (not Phase 1) — in shadow mode, preserving observation data matters more than strictness
- `added_by` / `added_date` attribution fields are **process controls** that belong in code review policy, not gate schema — defer to Phase 3
- Min-10-char reason requirement is **arbitrary and friction-generating** — drop entirely
- 50-entry hard limit should be a **soft warning threshold**, not a hard error — defer hard limit to Phase 2

**Debate outcome**: Add minimal schema (symbol + reason required, warn on malformed), add `whitelist_entries_applied: N` to frontmatter, drop attribution fields and character limits from v1.0 scope entirely.

---

## Convergence Score

| Recommendation | Panel Verdict | Debate Outcome | Delta |
|----------------|--------------|----------------|-------|
| BC-1 | BLOCKING | ADVISORY — spec text improved | Classification reduced, content validated |
| BC-2 | BLOCKING | ADVISORY — with `yaml.safe_dump()` | Classification reduced, fix retained |
| BC-3 | BLOCKING | SPLIT — coverage requirements block T06, fixture code does not | Narrowed, scope-corrected |
| NB-1 | NON-BLOCKING | NON-BLOCKING — v1.0 documentation + v1.1 algorithm | Confirmed, solution refined |
| NB-2 | NON-BLOCKING | NON-BLOCKING — tiered by enforcement phase | Confirmed, phased correctly |

**Convergence: 0.84** — high agreement on validity of underlying issues; significant reclassification of blocking severity for BC-1 and BC-2; scope corrections for BC-3.

**Unresolved conflicts: 0** — all recommendations reached a clear verdict.
