# Calibration C1 — blind re-grade of Reviewer Card R1 (opus-analyzer)

**Calibrator:** opus (claude-opus-4-7) per §11.3 fallback (disjoint set empty → degraded calibrator_diversity).
**Input seen:** Only `card-1-opus-analyzer.md`. No upstream investigative trail, no other reviewer cards.
**Reviewer's self-verdict:** PASS (1 HIGH, 3 MEDIUM, 0 CRITICAL).
**Reviewer's implicit confidence:** High (recommends ship-as-is with 2 clarifications).

---

## 5-Dimension Rubric Scores

### D1. Citation grounding — **4/5**

Spot-checked 8+ of the reviewer's citations directly against current source:

| Reviewer claim | Verified |
|---|---|
| `spec_parser.py:333 def extract_requirement_ids` | ✅ exact |
| `spec_parser.py:109 def parse_frontmatter` | ✅ exact |
| `executor.py:1947 def _build_steps` | ✅ exact |
| `executor.py:1899 def build_certify_step` | ✅ exact |
| `executor.py:2167 gate=None if config.convergence_enabled else SPEC_FIDELITY_GATE` | ✅ exact (token-for-token) |
| `fidelity_checker.py:287-303` fail-open block; smoking-gun `found=True, # fail-open` actually at L298 | ✅ block-boundary exact; reviewer self-flagged L298 vs L287 precision gap honestly |
| `fidelity_checker.py:314-337` partial-match; `found = True` at L316 | ✅ same pattern, reviewer self-flagged |
| `obligation_scanner.py:_DESCRIPTOR_NOUNS L109` | ✅ exact |
| `obligation_scanner.py` return-True stubs L719/L722/L725 | ✅ all three verified present in file |

**Justification (−1):** Reviewer's own −1 on fidelity_checker line-pin precision is fair self-assessment; I confirm it independently. Tasklist is reported as 832 lines, actual is 831 (trivial off-by-one). No fabricated citations detected. 4/5 stands.

### D2. Coverage completeness — **5/5** (coverage_pct = 1.00)

The 28-row coverage matrix (R0×3 + R1×6 + Acceptance×8 + Contract×10 = 27, plus R0-acceptance = 28) is concrete: each spec requirement names the exact phase/step that lands it. The Contract→test-filename mapping in D3 cross-confirms by anchoring all 10 contracts to specific test surface filenames. "Unmapped requirements: None" is justified by the matrix itself, not by assertion. The reviewer did not double-count, did not pad with phantom mappings, and did not skip the substrate-acceptance gates. 5/5.

### D3. Deviation-classification clarity — **5/5**

The HIGH/MEDIUM/CRITICAL severities are calibrated correctly. H-1 (R1.5/R1.6 fail-open window) is genuinely HIGH because it leaves master-flaw-1 partially intact for one release cycle inside the same plan that claims to invert the substrate; this is a substrate-leak finding, not a code-style nit. The 3 MEDIUMs are appropriately scoped: cadence-realism risk (M-1) is execution-feasibility not architectural, dispatch-walker corner-case (M-2) is a known-failure-mode risk in the new gate, and Contract #3 mechanism (M-3) is under-specification not absence. CRITICAL=0 is consistent with no flaw being structurally unaddressed. 5/5.

### D4. Risk-surface coverage — **5/5**

The per-master-flaw adequacy table is the strongest signal. Reviewer mapped each of master:§Flaws 1-5 to a specific structural fix (R1.3/R1.5 for Flaw 1; R1.4 for Flaw 2; R1.2 for Flaw 3; Contract #7 + R1.6 for Flaw 4; R0.3 + R1.1 for Flaw 5) and explicitly distinguished substrate-inversion fixes from downstream-validator patches. The H-1 finding itself is a risk-surface finding: it catches a transient substrate-leak that a less-rigorous reviewer would miss because both R1.5 and R1.6 individually look correct. Reviewer also audited the PRESERVE-target surface (4 targets × 3 protection layers) and the §Contract dispatch (all 10 items × specific test files). 5/5.

### D5. Recommendation actionability — **5/5**

"Ship-as-is with two pre-execution clarifications" is concrete:
- For H-1: two named alternatives — (a) annotate fail-open branches as "DELETED IN R1.6" + add PG10 parity assertion, OR (b) reorder R1.6 before R1.5 — with cost preference ("(a) is lower-cost").
- For M-1: explicit policy text proposed ("Sub-phases may run side-by-side dual-write *concurrently*, but each sub-phase's cutover decision is independent").
- For M-2: enumerate RoadmapConfig variants in walker.
- For M-3: name the deliverable shape (`.github/workflows/contract-3-generator-constraint.yml` or `make pr-lint-contract-3`).

Every finding has a file, a phase/step, and a remediation diff in narrative form. No prose-only handwaving. 5/5.

---

## Arithmetic mean → calibrated_confidence

(4 + 5 + 5 + 5 + 5) / 5 = **4.8 / 5 = 0.96**

---

## Adversarial sanity check

- Reviewer found 4 issues (1 HIGH + 3 MEDIUM), NOT zero — the "0-findings on an 831-line tasklist is suspicious" filter does not trigger.
- The HIGH finding is non-trivial and non-obvious: the R1.5/R1.6 ordering bug requires holding both phases in mind simultaneously and checking that the new fail-closed terminal supersedes the old fail-open before the old one is deleted. A surface reviewer would have given both phases individual PASS verdicts and missed the cross-phase substrate-leak window.
- Verdict PASS is internally consistent: 0 CRITICAL, 0 unmapped requirements, all 5 master flaws addressed structurally, all 4 PRESERVE targets honored at 3 protection layers, all 10 Contract items have named test surfaces. The plan does not warrant re-author.
- Reviewer's self-flagged D1 precision gap (line-pin on fidelity_checker) is the kind of honesty that argues *against* overconfidence — they could have claimed 5/5 on D1 and gotten away with it.

No anchoring penalty applied.

---

## Verdict-after-calibration: **PASS**

Concurs with reviewer's verdict. The 0.96 calibrated confidence reflects that this is a substantively grounded review with one minor citation-precision gap, not a structural problem. The reviewer's two pre-execution clarifications (H-1 fail-open window, M-1 parallelism policy) should be addressed before sprint kickoff but do not require restructuring the plan.

**Calibrator-flagged caveat:** §11.3 fallback applies — calibrator is same model class (opus) as reviewer, so calibrator_diversity is degraded. This calibration would be strengthened by a non-opus second calibrator if available.
